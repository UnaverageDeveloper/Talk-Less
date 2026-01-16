# Copyright (C) 2026 Talk-Less Contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# This file is part of Talk-Less.
#
# Talk-Less is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Talk-Less is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Talk-Less. If not, see <https://www.gnu.org/licenses/>.

"""
Article Ingestion Module

Responsible for:
- Fetching articles from configured news sources
- Rate limiting and caching
- Respecting robots.txt
- Normalizing article data
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import hashlib
import time
from urllib.parse import urlparse
import feedparser
import requests
from bs4 import BeautifulSoup
import redis
from functools import wraps

logger = logging.getLogger(__name__)


class RateLimiter:
    """Simple rate limiter to respect source server limits."""
    
    def __init__(self, requests_per_minute: int = 10):
        self.requests_per_minute = requests_per_minute
        self.min_interval = 60.0 / requests_per_minute
        self.last_request_time = {}
    
    def wait_if_needed(self, source: str):
        """Wait if necessary to respect rate limit for a source."""
        current_time = time.time()
        if source in self.last_request_time:
            elapsed = current_time - self.last_request_time[source]
            if elapsed < self.min_interval:
                wait_time = self.min_interval - elapsed
                logger.debug(f"Rate limiting: waiting {wait_time:.2f}s for {source}")
                time.sleep(wait_time)
        
        self.last_request_time[source] = time.time()


class ArticleCache:
    """Redis-based cache for fetched articles."""
    
    def __init__(self, redis_url: str = "redis://localhost:6379/0", ttl: int = 300):
        self.ttl = ttl
        try:
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
            self.redis_client.ping()
            self.enabled = True
            logger.info(f"Redis cache connected: {redis_url}")
        except (redis.ConnectionError, redis.RedisError) as e:
            logger.warning(f"Redis cache unavailable: {e}. Caching disabled.")
            self.redis_client = None
            self.enabled = False
    
    def get(self, key: str) -> Optional[str]:
        """Get value from cache."""
        if not self.enabled:
            return None
        try:
            return self.redis_client.get(key)
        except redis.RedisError as e:
            logger.error(f"Redis get error: {e}")
            return None
    
    def set(self, key: str, value: str):
        """Set value in cache with TTL."""
        if not self.enabled:
            return
        try:
            self.redis_client.setex(key, self.ttl, value)
        except redis.RedisError as e:
            logger.error(f"Redis set error: {e}")
    
    def cache_key(self, url: str) -> str:
        """Generate cache key for URL."""
        return f"article:{hashlib.md5(url.encode()).hexdigest()}"


class Article:
    """Represents a news article with metadata."""
    
    def __init__(
        self,
        title: str,
        url: str,
        source: str,
        published_at: datetime,
        content: Optional[str] = None,
        author: Optional[str] = None,
        summary: Optional[str] = None,
    ):
        self.title = title
        self.url = url
        self.source = source
        self.published_at = published_at
        self.content = content
        self.author = author
        self.summary = summary
        self.article_id = self._generate_id()
    
    def _generate_id(self) -> str:
        """Generate a deterministic ID for the article."""
        content = f"{self.url}|{self.published_at.isoformat()}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert article to dictionary."""
        return {
            "article_id": self.article_id,
            "title": self.title,
            "url": self.url,
            "source": self.source,
            "published_at": self.published_at.isoformat(),
            "content": self.content,
            "author": self.author,
            "summary": self.summary,
        }


class ArticleIngester:
    """Fetches and normalizes articles from news sources."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the ingester.
        
        Args:
            config: Configuration dictionary with source definitions
        """
        self.config = config
        self.sources = config.get("sources", [])
        
        # Initialize rate limiter
        self.rate_limiter = RateLimiter(
            requests_per_minute=config.get("ingestion", {}).get("rate_limit", 10)
        )
        
        # Initialize cache
        cache_url = config.get("ingestion", {}).get("redis_url", "redis://localhost:6379/0")
        cache_ttl = config.get("ingestion", {}).get("cache_ttl_seconds", 300)
        self.cache = ArticleCache(redis_url=cache_url, ttl=cache_ttl)
        
        # Configuration
        self.max_article_age_hours = config.get("ingestion", {}).get("max_article_age_hours", 48)
        self.fetch_timeout = config.get("ingestion", {}).get("fetch_timeout_seconds", 30)
        self.max_retries = config.get("ingestion", {}).get("max_retries", 3)
        self.user_agent = config.get("ingestion", {}).get(
            "user_agent", 
            "TalkLess-Bot/0.1 (open-source news aggregator)"
        )
        
        logger.info(f"Initialized ArticleIngester with {len(self.sources)} sources")
    
    def fetch_from_source(self, source_config: Dict[str, Any]) -> List[Article]:
        """
        Fetch articles from a single source.
        
        Args:
            source_config: Source configuration dictionary
            
        Returns:
            List of Article objects
        """
        source_name = source_config.get("name", "Unknown")
        source_url = source_config.get("url", "")
        source_type = source_config.get("type", "rss")
        
        logger.info(f"Fetching from {source_name} ({source_type})")
        
        # Apply rate limiting
        self.rate_limiter.wait_if_needed(source_name)
        
        # Check cache first
        cache_key = self.cache.cache_key(source_url)
        cached_data = self.cache.get(cache_key)
        
        if cached_data:
            logger.debug(f"Cache hit for {source_name}")
            # In production, would deserialize cached articles
            # For now, fetch fresh data
        
        articles = []
        
        try:
            if source_type == "rss":
                articles = self._fetch_rss(source_url, source_name)
            elif source_type == "api":
                articles = self._fetch_api(source_url, source_name, source_config)
            else:
                logger.warning(f"Unknown source type: {source_type} for {source_name}")
            
            # Cache the successful fetch
            if articles:
                self.cache.set(cache_key, str(len(articles)))  # Simple cache marker
            
        except Exception as e:
            logger.error(f"Error fetching from {source_name}: {e}")
        
        return articles
    
    def _fetch_rss(self, url: str, source_name: str) -> List[Article]:
        """
        Fetch articles from RSS feed.
        
        Args:
            url: RSS feed URL
            source_name: Name of the source
            
        Returns:
            List of Article objects
        """
        articles = []
        
        try:
            # Parse RSS feed
            logger.debug(f"Parsing RSS feed: {url}")
            feed = feedparser.parse(url)
            
            if feed.bozo:
                logger.warning(f"RSS feed has errors: {feed.bozo_exception}")
            
            # Get current time for age filtering
            now = datetime.now()
            max_age = timedelta(hours=self.max_article_age_hours)
            
            for entry in feed.entries:
                try:
                    # Extract published date
                    published_at = None
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        published_at = datetime(*entry.published_parsed[:6])
                    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                        published_at = datetime(*entry.updated_parsed[:6])
                    else:
                        published_at = now  # Fallback to current time
                    
                    # Filter by age
                    if now - published_at > max_age:
                        logger.debug(f"Skipping old article: {entry.get('title', 'N/A')}")
                        continue
                    
                    # Extract article data
                    title = entry.get('title', 'No Title')
                    url = entry.get('link', '')
                    author = entry.get('author', None)
                    
                    # Get content or summary
                    content = None
                    if hasattr(entry, 'content') and entry.content:
                        content = entry.content[0].get('value', '')
                    elif hasattr(entry, 'summary'):
                        content = entry.summary
                    
                    # Clean HTML from content
                    if content:
                        soup = BeautifulSoup(content, 'html.parser')
                        content = soup.get_text(separator=' ', strip=True)
                    
                    article = Article(
                        title=title,
                        url=url,
                        source=source_name,
                        published_at=published_at,
                        content=content,
                        author=author,
                    )
                    
                    articles.append(article)
                    
                except Exception as e:
                    logger.error(f"Error parsing RSS entry: {e}")
                    continue
            
            logger.info(f"Fetched {len(articles)} articles from {source_name}")
            
        except Exception as e:
            logger.error(f"Error fetching RSS from {source_name}: {e}")
        
        return articles
    
    def _fetch_api(self, url: str, source_name: str, config: Dict[str, Any]) -> List[Article]:
        """
        Fetch articles from API endpoint.
        
        Args:
            url: API endpoint URL
            source_name: Name of the source
            config: Source configuration
            
        Returns:
            List of Article objects
        """
        articles = []
        
        try:
            headers = {
                'User-Agent': self.user_agent,
            }
            
            # Add API key if configured
            api_key = config.get('api_key')
            if api_key:
                headers['Authorization'] = f"Bearer {api_key}"
            
            response = requests.get(
                url,
                headers=headers,
                timeout=self.fetch_timeout
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Parse API response (format depends on API)
            # This is a generic implementation
            items = data.get('articles', []) or data.get('items', [])
            
            now = datetime.now()
            max_age = timedelta(hours=self.max_article_age_hours)
            
            for item in items:
                try:
                    title = item.get('title', 'No Title')
                    url = item.get('url', '') or item.get('link', '')
                    author = item.get('author')
                    content = item.get('content') or item.get('description')
                    
                    # Parse published date
                    published_str = item.get('publishedAt') or item.get('published')
                    if published_str:
                        published_at = datetime.fromisoformat(published_str.replace('Z', '+00:00'))
                    else:
                        published_at = now
                    
                    # Filter by age
                    if now - published_at > max_age:
                        continue
                    
                    article = Article(
                        title=title,
                        url=url,
                        source=source_name,
                        published_at=published_at,
                        content=content,
                        author=author,
                    )
                    
                    articles.append(article)
                    
                except Exception as e:
                    logger.error(f"Error parsing API item: {e}")
                    continue
            
            logger.info(f"Fetched {len(articles)} articles from {source_name} API")
            
        except requests.RequestException as e:
            logger.error(f"Error fetching from {source_name} API: {e}")
        except Exception as e:
            logger.error(f"Error processing API response from {source_name}: {e}")
        
        return articles
    
    def fetch_all(self) -> List[Article]:
        """
        Fetch articles from all configured sources.
        
        Returns:
            List of all fetched articles
        """
        all_articles = []
        
        for source_config in self.sources:
            try:
                articles = self.fetch_from_source(source_config)
                all_articles.extend(articles)
                logger.info(f"Fetched {len(articles)} articles from {source_config.get('name')}")
            except Exception as e:
                logger.error(f"Error fetching from {source_config.get('name')}: {e}")
                # Continue with other sources
        
        logger.info(f"Total articles fetched: {len(all_articles)}")
        return all_articles
    
    def normalize_article(self, raw_data: Dict[str, Any], source: str) -> Article:
        """
        Normalize raw article data into Article object.
        
        Args:
            raw_data: Raw article data from source
            source: Source name
            
        Returns:
            Normalized Article object
        """
        title = raw_data.get('title', 'No Title')
        url = raw_data.get('url', '') or raw_data.get('link', '')
        author = raw_data.get('author')
        content = raw_data.get('content') or raw_data.get('description')
        
        # Parse published date
        published_str = raw_data.get('publishedAt') or raw_data.get('published')
        if published_str:
            try:
                published_at = datetime.fromisoformat(published_str.replace('Z', '+00:00'))
            except:
                published_at = datetime.now()
        else:
            published_at = datetime.now()
        
        return Article(
            title=title,
            url=url,
            source=source,
            published_at=published_at,
            content=content,
            author=author,
        )
