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
Article Comparison Module

Responsible for:
- Grouping articles by topic/event using embeddings
- Identifying perspective differences
- Detecting coverage gaps across sources
"""

import logging
from typing import List, Dict, Any, Set, Optional
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import DBSCAN
from collections import defaultdict
from .ingestion import Article

logger = logging.getLogger(__name__)


class ArticleGroup:
    """Represents a group of articles covering the same story."""
    
    def __init__(self, topic: str, articles: List[Article]):
        self.topic = topic
        self.articles = articles
        self.sources = self._extract_sources()
        self.group_id = self._generate_id()
    
    def _extract_sources(self) -> Set[str]:
        """Extract unique sources in this group."""
        return {article.source for article in self.articles}
    
    def _generate_id(self) -> str:
        """Generate deterministic ID for the group."""
        import hashlib
        # Use sorted article IDs for consistency
        article_ids = sorted([article.article_id for article in self.articles])
        content = "|".join(article_ids)
        return hashlib.md5(content.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert group to dictionary."""
        return {
            "group_id": self.group_id,
            "topic": self.topic,
            "article_count": len(self.articles),
            "sources": list(self.sources),
            "articles": [article.to_dict() for article in self.articles],
        }


class ArticleComparer:
    """Compares and groups articles by topic using semantic embeddings."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the comparer with embedding model.
        
        Args:
            config: Configuration dictionary with comparison settings
        """
        self.config = config
        self.similarity_threshold = config.get("similarity_threshold", 0.7)
        self.min_articles_per_group = config.get("min_articles_per_group", 2)
        self.max_articles_per_group = config.get("max_articles_per_group", 10)
        
        # Initialize embedding model (using lightweight model for speed)
        model_name = "all-MiniLM-L6-v2"  # Fast, good quality embeddings
        logger.info(f"Loading embedding model: {model_name}")
        self.embedding_model = SentenceTransformer(model_name)
        logger.info("Initialized ArticleComparer with embedding model")
    
    def group_by_topic(self, articles: List[Article]) -> List[ArticleGroup]:
        """
        Group articles that cover the same story using semantic similarity.
        
        Args:
            articles: List of articles to group
            
        Returns:
            List of ArticleGroup objects
        """
        if not articles:
            logger.info("No articles to group")
            return []
        
        logger.info(f"Grouping {len(articles)} articles by topic")
        
        # Generate embeddings for all articles
        texts = [self._prepare_text(article) for article in articles]
        logger.debug(f"Generating embeddings for {len(texts)} articles")
        embeddings = self.embedding_model.encode(texts, show_progress_bar=False)
        
        # Compute similarity matrix
        similarity_matrix = cosine_similarity(embeddings)
        
        # Use DBSCAN for clustering (density-based, handles noise well)
        # eps is derived from similarity threshold
        eps = 1 - self.similarity_threshold
        clusterer = DBSCAN(eps=eps, min_samples=self.min_articles_per_group, metric='precomputed')
        
        # Convert similarity to distance for DBSCAN
        distance_matrix = 1 - similarity_matrix
        cluster_labels = clusterer.fit_predict(distance_matrix)
        
        # Group articles by cluster
        clusters = defaultdict(list)
        for idx, label in enumerate(cluster_labels):
            if label != -1:  # -1 is noise in DBSCAN
                clusters[label].append(articles[idx])
        
        # Create ArticleGroup objects
        groups = []
        for cluster_id, cluster_articles in clusters.items():
            if len(cluster_articles) >= self.min_articles_per_group:
                # Limit group size if needed
                if len(cluster_articles) > self.max_articles_per_group:
                    logger.warning(f"Cluster {cluster_id} has {len(cluster_articles)} articles, "
                                 f"limiting to {self.max_articles_per_group}")
                    cluster_articles = cluster_articles[:self.max_articles_per_group]
                
                # Identify topic from articles
                topic = self._identify_topic(cluster_articles)
                group = ArticleGroup(topic=topic, articles=cluster_articles)
                groups.append(group)
                logger.debug(f"Created group '{topic}' with {len(cluster_articles)} articles "
                           f"from {len(group.sources)} sources")
        
        logger.info(f"Created {len(groups)} article groups from {len(articles)} articles")
        return groups
    
    def _prepare_text(self, article: Article) -> str:
        """
        Prepare article text for embedding.
        
        Args:
            article: Article to prepare
            
        Returns:
            Combined text for embedding
        """
        # Combine title and content (first 500 chars) for better context
        content_preview = article.content[:500] if article.content else ""
        return f"{article.title}. {content_preview}"
    
    def _identify_topic(self, articles: List[Article]) -> str:
        """
        Identify the main topic from a group of articles.
        
        Args:
            articles: List of articles in the group
            
        Returns:
            Topic string
        """
        # Simple heuristic: use title of article closest to centroid
        if not articles:
            return "Unknown Topic"
        
        if len(articles) == 1:
            return articles[0].title
        
        # Use first article's title as representative (can be improved)
        # In production, could use LLM to generate topic or extract common keywords
        return articles[0].title
    
    def compare_perspectives(self, group: ArticleGroup) -> Dict[str, Any]:
        """
        Analyze perspective differences within a group.
        
        Args:
            group: ArticleGroup to analyze
            
        Returns:
            Dictionary with perspective analysis
        """
        logger.info(f"Comparing perspectives for topic: {group.topic}")
        
        # Analyze sources
        source_coverage = {}
        for article in group.articles:
            source = article.source
            if source not in source_coverage:
                source_coverage[source] = {
                    "article_count": 0,
                    "titles": [],
                    "authors": []
                }
            source_coverage[source]["article_count"] += 1
            source_coverage[source]["titles"].append(article.title)
            if article.author:
                source_coverage[source]["authors"].append(article.author)
        
        # Identify unique perspectives
        perspectives = []
        for source, data in source_coverage.items():
            perspectives.append({
                "source": source,
                "article_count": data["article_count"],
                "unique_titles": len(set(data["titles"])),
                "authors": list(set(data["authors"]))
            })
        
        analysis = {
            "topic": group.topic,
            "group_id": group.group_id,
            "source_count": len(group.sources),
            "total_articles": len(group.articles),
            "perspectives": perspectives,
            "source_diversity": len(group.sources) / len(group.articles) if group.articles else 0,
        }
        
        logger.debug(f"Perspective analysis complete: {len(perspectives)} perspectives found")
        return analysis
    
    def find_coverage_gaps(self, groups: List[ArticleGroup], all_sources: Set[str]) -> List[Dict[str, Any]]:
        """
        Identify stories covered by some sources but not others.
        
        Args:
            groups: List of article groups
            all_sources: Set of all configured source names
            
        Returns:
            List of coverage gap analyses
        """
        logger.info(f"Finding coverage gaps across {len(all_sources)} configured sources")
        
        gaps = []
        
        for group in groups:
            sources_in_group = group.sources
            missing_sources = all_sources - sources_in_group
            
            if missing_sources:
                gap = {
                    "topic": group.topic,
                    "group_id": group.group_id,
                    "covered_by": list(sources_in_group),
                    "missing_from": list(missing_sources),
                    "coverage_percentage": len(sources_in_group) / len(all_sources) * 100
                }
                gaps.append(gap)
                logger.debug(f"Gap found: '{group.topic}' missing from {len(missing_sources)} sources")
        
        logger.info(f"Found {len(gaps)} coverage gaps")
        return gaps
