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
Pipeline Runner

Main entry point for running the news processing pipeline.
"""

import logging
import sys
from pathlib import Path
from typing import Dict, Any
import yaml

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from pipeline.ingestion import ArticleIngester
from pipeline.comparison import ArticleComparer
from pipeline.summarization import ArticleSummarizer
from pipeline.bias_detection import BiasDetector

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_config() -> Dict[str, Any]:
    """Load pipeline configuration."""
    config_dir = backend_dir / "config"
    
    # Load all config files
    configs = {}
    
    config_files = {
        "sources": config_dir / "sources.yaml",
        "bias_indicators": config_dir / "bias_indicators.yaml",
        "pipeline": config_dir / "pipeline_config.yaml",
    }
    
    for key, config_file in config_files.items():
        if config_file.exists():
            with open(config_file, 'r') as f:
                configs[key] = yaml.safe_load(f)
            logger.info(f"Loaded config: {key}")
        else:
            logger.warning(f"Config file not found: {config_file}")
            configs[key] = {}
    
    return configs


def run_pipeline():
    """Run the complete pipeline."""
    logger.info("=" * 60)
    logger.info("Starting Talk-Less Pipeline")
    logger.info("=" * 60)
    
    # Load configuration
    logger.info("Loading configuration...")
    configs = load_config()
    
    # Initialize components
    logger.info("Initializing pipeline components...")
    ingester = ArticleIngester(configs["sources"])
    comparer = ArticleComparer(configs["pipeline"].get("comparison", {}))
    summarizer = ArticleSummarizer(configs["pipeline"].get("summarization", {}))
    bias_detector = BiasDetector(configs["bias_indicators"])
    
    # Stage 1: Ingestion
    logger.info("Stage 1: Fetching articles from sources...")
    articles = ingester.fetch_all()
    
    if not articles:
        logger.warning("No articles fetched. Pipeline will exit.")
        return
    
    logger.info(f"Fetched {len(articles)} articles")
    
    # Stage 2: Bias Detection on Individual Articles
    logger.info("Stage 2: Detecting bias in articles...")
    article_bias = {}
    for article in articles:
        indicators = bias_detector.detect_bias(article)
        if indicators:
            article_bias[article.article_id] = indicators
    
    logger.info(f"Detected bias indicators in {len(article_bias)} articles")
    
    # Stage 3: Grouping and Comparison
    logger.info("Stage 3: Grouping articles by topic...")
    groups = comparer.group_by_topic(articles)
    
    if not groups:
        logger.warning("No article groups created. Pipeline will exit.")
        return
    
    logger.info(f"Created {len(groups)} article groups")
    
    # Stage 4: Perspective Analysis
    logger.info("Stage 4: Analyzing perspectives...")
    perspective_analyses = {}
    for group in groups:
        analysis = comparer.compare_perspectives(group)
        perspective_analyses[group.topic] = analysis
    
    # Stage 5: Summarization
    logger.info("Stage 5: Generating summaries...")
    summaries = []
    for group in groups:
        try:
            perspective_analysis = perspective_analyses.get(group.topic, {})
            summary = summarizer.generate_summary(group, perspective_analysis)
            
            if summarizer.validate_summary(summary):
                summaries.append(summary)
                logger.info(f"Generated summary for: {group.topic}")
            else:
                logger.warning(f"Summary validation failed for: {group.topic}")
        except Exception as e:
            logger.error(f"Error generating summary for {group.topic}: {e}")
    
    logger.info(f"Generated {len(summaries)} summaries")
    
    # Stage 6: Transparency Report
    logger.info("Stage 6: Generating transparency report...")
    transparency_report = bias_detector.generate_transparency_report(
        articles, article_bias
    )
    
    # Stage 7: Output
    logger.info("Stage 7: Storing results...")
    # TODO: Store summaries in database
    # TODO: Export public data
    # TODO: Update cache
    
    logger.info("=" * 60)
    logger.info("Pipeline completed successfully")
    logger.info(f"  Articles processed: {len(articles)}")
    logger.info(f"  Article groups: {len(groups)}")
    logger.info(f"  Summaries generated: {len(summaries)}")
    logger.info(f"  Bias indicators found: {len(article_bias)}")
    logger.info("=" * 60)


if __name__ == "__main__":
    try:
        run_pipeline()
    except KeyboardInterrupt:
        logger.info("Pipeline interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Pipeline failed with error: {e}", exc_info=True)
        sys.exit(1)
