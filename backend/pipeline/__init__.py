"""
News Pipeline Package

This package contains the core news processing pipeline:
- Ingestion: Fetching articles from configured sources
- Comparison: Grouping and comparing articles by topic
- Summarization: Generating transformative summaries with citations
- Bias Detection: Identifying and documenting bias patterns
"""

# Components will be imported when needed to avoid circular dependencies
__all__ = [
    "ArticleIngester",
    "ArticleComparer",
    "ArticleSummarizer",
    "BiasDetector",
]
