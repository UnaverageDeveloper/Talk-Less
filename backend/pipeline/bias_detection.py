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
Bias Detection Module

Responsible for:
- Detecting bias indicators in articles using rules
- Documenting bias patterns
- Flagging problematic language
- Creating transparency reports
"""

import logging
import re
import yaml
from typing import List, Dict, Any, Set, Optional
from pathlib import Path
from .ingestion import Article

logger = logging.getLogger(__name__)


class BiasIndicator:
    """Represents a detected bias indicator."""
    
    def __init__(
        self,
        indicator_type: str,
        description: str,
        confidence: str,
        examples: List[str],
        category: Optional[str] = None,
        rationale: Optional[str] = None,
    ):
        self.indicator_type = indicator_type
        self.description = description
        self.confidence = confidence
        self.examples = examples
        self.category = category
        self.rationale = rationale
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert indicator to dictionary."""
        result = {
            "type": self.indicator_type,
            "description": self.description,
            "confidence": self.confidence,
            "examples": self.examples,
        }
        if self.category:
            result["category"] = self.category
        if self.rationale:
            result["rationale"] = self.rationale
        return result


class BiasDetector:
    """Detects and documents bias in articles using configurable rules."""
    
    def __init__(self, config: Dict[str, Any], rules_file: Optional[str] = None):
        """
        Initialize the bias detector with rules.
        
        Args:
            config: Configuration with bias detection settings
            rules_file: Path to bias_indicators.yaml file
        """
        self.config = config
        self.enabled = config.get("enabled", True)
        self.min_confidence = config.get("min_confidence", "low")
        self.context_window = 50  # words before/after for context
        
        # Load bias detection rules
        if rules_file is None:
            # Default path
            rules_file = str(Path(__file__).parent.parent / "config" / "bias_indicators.yaml")
        
        self.rules = self._load_rules(rules_file)
        self.loaded_words = self._extract_loaded_words()
        self.attribution_patterns = self._extract_attribution_patterns()
        self.weights = self.rules.get("settings", {}).get("weights", {})
        
        logger.info(f"Initialized BiasDetector with {len(self.loaded_words)} loaded words "
                   f"and {len(self.attribution_patterns)} attribution patterns")
    
    def _load_rules(self, rules_file: str) -> Dict[str, Any]:
        """Load bias detection rules from YAML file."""
        try:
            with open(rules_file, 'r') as f:
                rules = yaml.safe_load(f)
            logger.debug(f"Loaded bias rules from {rules_file}")
            return rules
        except Exception as e:
            logger.error(f"Failed to load bias rules: {e}")
            return {}
    
    def _extract_loaded_words(self) -> List[Dict[str, str]]:
        """Extract emotionally loaded words from rules."""
        loaded_words = self.rules.get("loaded_words", [])
        return loaded_words
    
    def _extract_attribution_patterns(self) -> List[Dict[str, str]]:
        """Extract attribution patterns from rules."""
        attribution = self.rules.get("attribution_issues", [])
        return attribution
    
    def detect_bias(self, article: Article) -> List[BiasIndicator]:
        """
        Detect bias indicators in an article.
        
        Args:
            article: Article to analyze
            
        Returns:
            List of detected BiasIndicator objects
        """
        if not self.enabled:
            return []
        
        logger.debug(f"Detecting bias in article: {article.title}")
        
        indicators = []
        scores = {}  # Track scores by category
        
        # Check for loaded language
        loaded_indicators = self._check_loaded_language(article)
        if loaded_indicators:
            indicators.extend(loaded_indicators)
            scores["loaded_words"] = len(loaded_indicators)
        
        # Check attribution quality
        attribution_indicators = self._check_attribution(article)
        if attribution_indicators:
            indicators.extend(attribution_indicators)
            scores["attribution_issues"] = len(attribution_indicators)
        
        # Check framing
        framing_indicators = self._check_framing(article)
        if framing_indicators:
            indicators.extend(framing_indicators)
            scores["framing_patterns"] = len(framing_indicators)
        
        # Calculate overall confidence based on weighted scores
        total_score = 0
        for category, count in scores.items():
            weight = self.weights.get(category, 1.0)
            total_score += count * weight
        
        # Filter by minimum confidence
        confidence_thresholds = self.rules.get("settings", {}).get("confidence_levels", {})
        high_threshold = confidence_thresholds.get("high", 3.0)
        medium_threshold = confidence_thresholds.get("medium", 1.5)
        low_threshold = confidence_thresholds.get("low", 0.5)
        
        # Assign overall confidence to indicators
        if total_score >= high_threshold:
            overall_confidence = "high"
        elif total_score >= medium_threshold:
            overall_confidence = "medium"
        elif total_score >= low_threshold:
            overall_confidence = "low"
        else:
            overall_confidence = "none"
        
        # Filter by configured minimum confidence
        min_conf_order = ["low", "medium", "high"]
        min_conf_idx = min_conf_order.index(self.min_confidence)
        if overall_confidence != "none":
            overall_conf_idx = min_conf_order.index(overall_confidence)
            if overall_conf_idx < min_conf_idx:
                logger.debug(f"Filtered out indicators: {overall_confidence} < {self.min_confidence}")
                return []
        
        logger.debug(f"Found {len(indicators)} bias indicators (score: {total_score:.1f}, "
                    f"confidence: {overall_confidence})")
        return indicators
    
    def _check_loaded_language(self, article: Article) -> List[BiasIndicator]:
        """
        Check for emotionally loaded language.
        
        Args:
            article: Article to check
            
        Returns:
            List of BiasIndicators found
        """
        if not article.content and not article.title:
            return []
        
        indicators = []
        text = f"{article.title} {article.content or ''}"
        text_lower = text.lower()
        words = text_lower.split()
        
        for word_rule in self.loaded_words:
            word = word_rule.get("word", "").lower()
            category = word_rule.get("category", "unknown")
            rationale = word_rule.get("rationale", "")
            
            # Find occurrences
            pattern = r'\b' + re.escape(word) + r'\b'
            matches = list(re.finditer(pattern, text_lower))
            
            if matches:
                examples = []
                for match in matches[:3]:  # Limit to 3 examples
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + 50)
                    context = text[start:end]
                    examples.append(f"...{context}...")
                
                indicator = BiasIndicator(
                    indicator_type="loaded_language",
                    description=f"Emotionally loaded word: '{word}'",
                    confidence="medium",
                    examples=examples,
                    category=category,
                    rationale=rationale
                )
                indicators.append(indicator)
                logger.debug(f"Found loaded word '{word}' {len(matches)} time(s)")
        
        return indicators
    
    def _check_attribution(self, article: Article) -> List[BiasIndicator]:
        """
        Check quality of source attribution.
        
        Args:
            article: Article to check
            
        Returns:
            List of BiasIndicators found
        """
        if not article.content:
            return []
        
        indicators = []
        text = article.content.lower()
        
        for attr_rule in self.attribution_patterns:
            pattern = attr_rule.get("pattern", "")
            issue = attr_rule.get("issue", "")
            rationale = attr_rule.get("rationale", "")
            
            # Find occurrences
            matches = list(re.finditer(re.escape(pattern.lower()), text))
            
            if matches:
                examples = []
                for match in matches[:3]:  # Limit to 3 examples
                    start = max(0, match.start() - 50)
                    end = min(len(article.content), match.end() + 50)
                    context = article.content[start:end]
                    examples.append(f"...{context}...")
                
                indicator = BiasIndicator(
                    indicator_type="attribution_issue",
                    description=f"Weak attribution: '{pattern}' ({issue})",
                    confidence="medium",
                    examples=examples,
                    category=issue,
                    rationale=rationale
                )
                indicators.append(indicator)
                logger.debug(f"Found attribution issue '{pattern}' {len(matches)} time(s)")
        
        return indicators
    
    def _check_framing(self, article: Article) -> List[BiasIndicator]:
        """
        Check for biased framing.
        
        Args:
            article: Article to check
            
        Returns:
            List of BiasIndicators found
        """
        if not article.content:
            return []
        
        indicators = []
        
        # Check for headline vs body mismatch (basic check)
        if article.title and article.content:
            title_words = set(article.title.lower().split())
            content_words = set(article.content.lower().split()[:100])  # First 100 words
            
            # If title has strong claims not in first part of body
            strong_words = {"shocking", "stunning", "outrage", "bombshell", "explosive"}
            title_strong = title_words & strong_words
            
            if title_strong and not (title_strong & content_words):
                indicator = BiasIndicator(
                    indicator_type="framing_issue",
                    description="Headline uses strong language not found in article opening",
                    confidence="low",
                    examples=[article.title],
                    category="headline_framing",
                    rationale="May indicate clickbait or emphasis bias"
                )
                indicators.append(indicator)
                logger.debug("Found potential headline framing issue")
        
        return indicators
    
    def generate_transparency_report(
        self,
        articles: List[Article],
        indicators_per_article: Dict[str, List[BiasIndicator]],
    ) -> Dict[str, Any]:
        """
        Generate a transparency report on detected bias.
        
        Args:
            articles: List of articles analyzed
            indicators_per_article: Mapping of article IDs to indicators
            
        Returns:
            Transparency report dictionary
        """
        logger.info("Generating bias transparency report")
        
        # Count indicators by type
        indicator_types = {}
        indicator_categories = {}
        source_breakdown = {}
        
        for article_id, indicators in indicators_per_article.items():
            # Find corresponding article
            article = next((a for a in articles if a.article_id == article_id), None)
            if not article:
                continue
            
            source = article.source
            if source not in source_breakdown:
                source_breakdown[source] = {
                    "articles_analyzed": 0,
                    "articles_with_indicators": 0,
                    "total_indicators": 0,
                }
            
            source_breakdown[source]["articles_analyzed"] += 1
            
            if indicators:
                source_breakdown[source]["articles_with_indicators"] += 1
                source_breakdown[source]["total_indicators"] += len(indicators)
                
                for indicator in indicators:
                    # Count by type
                    ind_type = indicator.indicator_type
                    indicator_types[ind_type] = indicator_types.get(ind_type, 0) + 1
                    
                    # Count by category
                    if indicator.category:
                        indicator_categories[indicator.category] = \
                            indicator_categories.get(indicator.category, 0) + 1
        
        report = {
            "total_articles": len(articles),
            "articles_with_indicators": len(indicators_per_article),
            "total_indicators": sum(len(v) for v in indicators_per_article.values()),
            "indicator_types": indicator_types,
            "indicator_categories": indicator_categories,
            "source_breakdown": source_breakdown,
            "rules_version": self.rules.get("version", "unknown"),
            "detection_enabled": self.enabled,
            "min_confidence_threshold": self.min_confidence,
        }
        
        logger.info(f"Transparency report complete: {report['articles_with_indicators']}/"
                   f"{report['total_articles']} articles with indicators")
        return report
