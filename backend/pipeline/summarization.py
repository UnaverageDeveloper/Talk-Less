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
Article Summarization Module

Responsible for:
- Generating transformative summaries using LLM (not excerpts)
- Citing all claims to sources
- Including multiple perspectives
- Ensuring summaries are legally distinct from source material
"""

import logging
import os
import re
from typing import List, Dict, Any, Optional
from datetime import datetime
import openai
from anthropic import Anthropic
from .comparison import ArticleGroup

logger = logging.getLogger(__name__)


class Summary:
    """Represents a generated news summary."""
    
    def __init__(
        self,
        topic: str,
        summary_text: str,
        sources: List[Dict[str, str]],
        perspectives: List[Dict[str, Any]],
        created_at: str,
        confidence: str = "medium",
        group_id: Optional[str] = None,
    ):
        self.topic = topic
        self.summary_text = summary_text
        self.sources = sources
        self.perspectives = perspectives
        self.created_at = created_at
        self.confidence = confidence
        self.group_id = group_id
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert summary to dictionary."""
        return {
            "topic": self.topic,
            "summary": self.summary_text,
            "sources": self.sources,
            "perspectives": self.perspectives,
            "created_at": self.created_at,
            "confidence": self.confidence,
            "group_id": self.group_id,
        }


class ArticleSummarizer:
    """Generates summaries from article groups using LLM."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the summarizer with LLM credentials.
        
        Args:
            config: Configuration dictionary with LLM settings
        """
        self.config = config
        self.model = config.get("model", "gpt-4")
        self.temperature = config.get("temperature", 0.3)  # Low for consistency
        self.max_summary_length = config.get("max_summary_length", 1000)
        self.min_summary_length = config.get("min_summary_length", 200)
        self.require_citations = config.get("require_citations", True)
        self.max_retries = config.get("max_retries", 2)
        
        # Initialize LLM clients
        self.openai_client = None
        self.anthropic_client = None
        
        if "gpt" in self.model.lower():
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                openai.api_key = api_key
                self.openai_client = openai
                logger.info(f"Initialized ArticleSummarizer with OpenAI model: {self.model}")
            else:
                logger.warning("OPENAI_API_KEY not set, summarization will fail")
        
        elif "claude" in self.model.lower():
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if api_key:
                self.anthropic_client = Anthropic(api_key=api_key)
                logger.info(f"Initialized ArticleSummarizer with Anthropic model: {self.model}")
            else:
                logger.warning("ANTHROPIC_API_KEY not set, summarization will fail")
        else:
            logger.warning(f"Unknown model: {self.model}, summarization may fail")
    
    def generate_summary(
        self,
        group: ArticleGroup,
        perspective_analysis: Dict[str, Any],
    ) -> Optional[Summary]:
        """
        Generate a transformative summary for an article group.
        
        Args:
            group: ArticleGroup to summarize
            perspective_analysis: Analysis of perspectives from comparer
            
        Returns:
            Summary object or None if generation fails
        """
        logger.info(f"Generating summary for topic: {group.topic}")
        
        # Build comprehensive prompt
        prompt = self._build_prompt(group, perspective_analysis)
        
        # Generate summary with retries
        for attempt in range(self.max_retries + 1):
            try:
                logger.debug(f"Summary generation attempt {attempt + 1}/{self.max_retries + 1}")
                
                # Call LLM
                summary_text = self._call_llm(prompt)
                
                if not summary_text:
                    logger.error("LLM returned empty summary")
                    continue
                
                # Extract citations from summary
                sources = self._extract_sources(summary_text, group)
                
                # Create summary object
                summary = Summary(
                    topic=group.topic,
                    summary_text=summary_text,
                    sources=sources,
                    perspectives=perspective_analysis.get("perspectives", []),
                    created_at=datetime.utcnow().isoformat() + "Z",
                    group_id=group.group_id,
                )
                
                # Validate summary
                if self.validate_summary(summary, group):
                    logger.info(f"Successfully generated summary for: {group.topic}")
                    return summary
                else:
                    logger.warning(f"Summary validation failed, attempt {attempt + 1}")
                    
            except Exception as e:
                logger.error(f"Error generating summary (attempt {attempt + 1}): {e}")
        
        logger.error(f"Failed to generate valid summary after {self.max_retries + 1} attempts")
        return None
    
    def _build_prompt(
        self,
        group: ArticleGroup,
        perspective_analysis: Dict[str, Any],
    ) -> str:
        """
        Build comprehensive prompt for LLM summarization.
        
        Args:
            group: ArticleGroup to summarize
            perspective_analysis: Perspective analysis
            
        Returns:
            Prompt string
        """
        # Build articles section
        articles_text = ""
        for idx, article in enumerate(group.articles, 1):
            articles_text += f"\n[Article {idx}]\n"
            articles_text += f"Source: {article.source}\n"
            articles_text += f"Title: {article.title}\n"
            if article.author:
                articles_text += f"Author: {article.author}\n"
            articles_text += f"URL: {article.url}\n"
            if article.content:
                # Limit content length to avoid token limits
                content = article.content[:2000]
                articles_text += f"Content: {content}\n"
            articles_text += "\n"
        
        # Build perspectives section
        perspectives_text = ""
        for perspective in perspective_analysis.get("perspectives", []):
            perspectives_text += f"- {perspective['source']}: {perspective['article_count']} article(s)\n"
        
        prompt = f"""You are a news summarization system for Talk-Less, an open-source public-good news platform. Your task is to create a transformative, unbiased summary of multiple news articles covering the same story.

CRITICAL REQUIREMENTS (NON-NEGOTIABLE):
1. Write ORIGINAL text - do NOT copy or excerpt from sources
2. Cite EVERY factual claim with [Source: <source name>]
3. Include ALL perspectives found in the articles
4. Do NOT add speculation, opinion, or analysis
5. Note conflicting information when sources disagree
6. Use neutral, factual language only
7. Length: {self.min_summary_length}-{self.max_summary_length} characters
8. If sources conflict, present both views with citations

LEGAL REQUIREMENT:
Your summary must be transformative and legally distinct from the source material. Rewrite information in your own words, never copy sentences or unique phrases from articles.

ARTICLES TO SUMMARIZE:
{articles_text}

PERSPECTIVE ANALYSIS:
Sources covering this story:
{perspectives_text}

Total articles: {len(group.articles)}
Unique sources: {len(group.sources)}

OUTPUT FORMAT:
Write a cohesive narrative summary that synthesizes all articles. Use [Source: <name>] after each claim to cite which source reported it. If multiple sources report the same fact, list all: [Sources: X, Y].

Begin your summary now:"""
        
        return prompt
    
    def _call_llm(self, prompt: str) -> Optional[str]:
        """
        Call the configured LLM to generate summary.
        
        Args:
            prompt: The prompt to send to the LLM
            
        Returns:
            Generated summary text or None if failed
        """
        try:
            if "gpt" in self.model.lower() and self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a precise, unbiased news summarization system."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self.temperature,
                    max_tokens=2000,
                )
                return response.choices[0].message.content.strip()
            
            elif "claude" in self.model.lower() and self.anthropic_client:
                response = self.anthropic_client.messages.create(
                    model=self.model,
                    max_tokens=2000,
                    temperature=self.temperature,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                return response.content[0].text.strip()
            
            else:
                logger.error(f"No valid LLM client configured for model: {self.model}")
                return None
                
        except Exception as e:
            logger.error(f"LLM API call failed: {e}")
            return None
    
    def _extract_sources(self, summary_text: str, group: ArticleGroup) -> List[Dict[str, str]]:
        """
        Extract cited sources from summary.
        
        Args:
            summary_text: The generated summary
            group: ArticleGroup being summarized
            
        Returns:
            List of source dictionaries
        """
        sources = []
        sources_dict = {}
        
        # Build mapping of source names to articles
        for article in group.articles:
            if article.source not in sources_dict:
                sources_dict[article.source] = {
                    "name": article.source,
                    "url": article.url,
                    "title": article.title
                }
        
        # Extract cited sources from summary (look for [Source: X] patterns)
        cited_sources = set()
        patterns = [
            r'\[Source: ([^\]]+)\]',
            r'\[Sources: ([^\]]+)\]',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, summary_text)
            for match in matches:
                # Handle multiple sources
                source_names = [s.strip() for s in match.split(',')]
                cited_sources.update(source_names)
        
        # Build sources list
        for source_name in cited_sources:
            if source_name in sources_dict:
                sources.append(sources_dict[source_name])
        
        return sources
    
    def validate_summary(self, summary: Summary, group: ArticleGroup) -> bool:
        """
        Validate that summary meets requirements.
        
        Args:
            summary: Summary to validate
            group: Original article group
            
        Returns:
            True if valid, False otherwise
        """
        text = summary.summary_text
        
        # Check length
        if len(text) < self.min_summary_length:
            logger.warning(f"Summary too short: {len(text)} < {self.min_summary_length}")
            return False
        
        if len(text) > self.max_summary_length:
            logger.warning(f"Summary too long: {len(text)} > {self.max_summary_length}")
            return False
        
        # Check for citations if required
        if self.require_citations:
            citation_pattern = r'\[Sources?:'
            citations = re.findall(citation_pattern, text)
            if len(citations) < 3:  # At least 3 citations expected
                logger.warning(f"Insufficient citations: {len(citations)} < 3")
                return False
        
        # Check that summary doesn't copy exact phrases from sources
        # (Simple check: look for long matching sequences)
        for article in group.articles:
            if article.content:
                # Check for copied phrases (10+ words in a row)
                words_in_summary = text.lower().split()
                words_in_article = article.content.lower().split()
                
                for i in range(len(words_in_summary) - 10):
                    phrase = ' '.join(words_in_summary[i:i+10])
                    if phrase in ' '.join(words_in_article):
                        logger.warning("Summary appears to copy text from source")
                        return False
        
        logger.debug("Summary validation passed")
        return True
