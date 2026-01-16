"""
Unit Tests for Pipeline Components

Tests for ingestion, comparison, summarization, and bias detection modules.
"""

import pytest
from datetime import datetime
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from pipeline.ingestion import Article, ArticleIngester
from pipeline.comparison import ArticleGroup, ArticleComparer
from pipeline.summarization import Summary, ArticleSummarizer
from pipeline.bias_detection import BiasIndicator, BiasDetector


class TestArticle:
    """Tests for Article data model."""
    
    def test_article_creation(self):
        """Test creating an article with all fields."""
        article = Article(
            title="Test Article",
            url="https://example.com/article",
            source="Test Source",
            published_at=datetime.now(),
            content="Test content",
            author="Test Author",
        )
        
        assert article.title == "Test Article"
        assert article.url == "https://example.com/article"
        assert article.source == "Test Source"
        assert article.content == "Test content"
        assert article.author == "Test Author"
        assert article.article_id is not None
        assert len(article.article_id) == 16
    
    def test_article_id_is_deterministic(self):
        """Test that article ID is deterministic based on URL and timestamp."""
        timestamp = datetime(2026, 1, 1, 12, 0, 0)
        
        article1 = Article(
            title="Test",
            url="https://example.com/test",
            source="Source",
            published_at=timestamp,
        )
        
        article2 = Article(
            title="Different Title",  # Title doesn't affect ID
            url="https://example.com/test",
            source="Source",
            published_at=timestamp,
        )
        
        assert article1.article_id == article2.article_id
    
    def test_article_to_dict(self):
        """Test converting article to dictionary."""
        article = Article(
            title="Test Article",
            url="https://example.com/article",
            source="Test Source",
            published_at=datetime(2026, 1, 1, 12, 0, 0),
        )
        
        article_dict = article.to_dict()
        
        assert article_dict['title'] == "Test Article"
        assert article_dict['url'] == "https://example.com/article"
        assert article_dict['source'] == "Test Source"
        assert 'article_id' in article_dict
        assert 'published_at' in article_dict


class TestArticleIngester:
    """Tests for ArticleIngester."""
    
    def test_ingester_initialization(self):
        """Test initializing ingester with config."""
        config = {
            'sources': [
                {'name': 'Source A', 'url': 'https://example.com/rss'},
                {'name': 'Source B', 'url': 'https://example.org/rss'},
            ]
        }
        
        ingester = ArticleIngester(config)
        
        assert len(ingester.sources) == 2
        assert ingester.sources[0]['name'] == 'Source A'
    
    def test_fetch_all_returns_list(self):
        """Test that fetch_all returns a list (even if empty)."""
        config = {'sources': []}
        ingester = ArticleIngester(config)
        
        articles = ingester.fetch_all()
        
        assert isinstance(articles, list)


class TestArticleComparer:
    """Tests for ArticleComparer."""
    
    def test_comparer_initialization(self):
        """Test initializing comparer with config."""
        config = {'similarity_threshold': 0.8}
        comparer = ArticleComparer(config)
        
        assert comparer.similarity_threshold == 0.8
    
    def test_group_by_topic_returns_list(self):
        """Test that group_by_topic returns a list."""
        config = {}
        comparer = ArticleComparer(config)
        
        groups = comparer.group_by_topic([])
        
        assert isinstance(groups, list)


class TestArticleSummarizer:
    """Tests for ArticleSummarizer."""
    
    def test_summarizer_initialization(self):
        """Test initializing summarizer with config."""
        config = {
            'model': 'gpt-4',
            'temperature': 0.3,
        }
        
        summarizer = ArticleSummarizer(config)
        
        assert summarizer.model == 'gpt-4'
        assert summarizer.temperature == 0.3


class TestBiasDetector:
    """Tests for BiasDetector."""
    
    def test_detector_initialization(self):
        """Test initializing bias detector with config."""
        config = {}
        detector = BiasDetector(config)
        
        assert detector.config == config
    
    def test_detect_bias_returns_list(self):
        """Test that detect_bias returns a list."""
        config = {}
        detector = BiasDetector(config)
        
        article = Article(
            title="Test",
            url="https://example.com/test",
            source="Test Source",
            published_at=datetime.now(),
            content="Test content",
        )
        
        indicators = detector.detect_bias(article)
        
        assert isinstance(indicators, list)


class TestBiasIndicator:
    """Tests for BiasIndicator data model."""
    
    def test_bias_indicator_creation(self):
        """Test creating a bias indicator."""
        indicator = BiasIndicator(
            indicator_type="loaded_language",
            description="Uses emotionally charged words",
            confidence="high",
            examples=["slammed", "blasted"],
        )
        
        assert indicator.indicator_type == "loaded_language"
        assert indicator.description == "Uses emotionally charged words"
        assert indicator.confidence == "high"
        assert len(indicator.examples) == 2
    
    def test_bias_indicator_to_dict(self):
        """Test converting indicator to dictionary."""
        indicator = BiasIndicator(
            indicator_type="loaded_language",
            description="Test description",
            confidence="medium",
            examples=["example"],
        )
        
        indicator_dict = indicator.to_dict()
        
        assert indicator_dict['type'] == "loaded_language"
        assert indicator_dict['description'] == "Test description"
        assert indicator_dict['confidence'] == "medium"
        assert indicator_dict['examples'] == ["example"]


class TestSummary:
    """Tests for Summary data model."""
    
    def test_summary_creation(self):
        """Test creating a summary."""
        summary = Summary(
            topic="Test Topic",
            summary_text="This is a test summary.",
            sources=[],
            perspectives=[],
            created_at="2026-01-01T00:00:00Z",
        )
        
        assert summary.topic == "Test Topic"
        assert summary.summary_text == "This is a test summary."
        assert isinstance(summary.sources, list)
        assert isinstance(summary.perspectives, list)
    
    def test_summary_to_dict(self):
        """Test converting summary to dictionary."""
        summary = Summary(
            topic="Test Topic",
            summary_text="Test summary text",
            sources=[{"name": "Source A", "url": "https://example.com"}],
            perspectives=[],
            created_at="2026-01-01T00:00:00Z",
        )
        
        summary_dict = summary.to_dict()
        
        assert summary_dict['topic'] == "Test Topic"
        assert summary_dict['summary'] == "Test summary text"
        assert len(summary_dict['sources']) == 1


class TestArticleGroup:
    """Tests for ArticleGroup data model."""
    
    def test_article_group_creation(self):
        """Test creating an article group."""
        articles = [
            Article(
                title="Article 1",
                url="https://example.com/1",
                source="Source A",
                published_at=datetime.now(),
            ),
            Article(
                title="Article 2",
                url="https://example.com/2",
                source="Source B",
                published_at=datetime.now(),
            ),
        ]
        
        group = ArticleGroup("Test Topic", articles)
        
        assert group.topic == "Test Topic"
        assert len(group.articles) == 2
        assert len(group.sources) == 2
        assert "Source A" in group.sources
        assert "Source B" in group.sources
    
    def test_article_group_to_dict(self):
        """Test converting article group to dictionary."""
        articles = [
            Article(
                title="Test Article",
                url="https://example.com/test",
                source="Test Source",
                published_at=datetime.now(),
            ),
        ]
        
        group = ArticleGroup("Test Topic", articles)
        group_dict = group.to_dict()
        
        assert group_dict['topic'] == "Test Topic"
        assert group_dict['article_count'] == 1
        assert len(group_dict['sources']) == 1
        assert len(group_dict['articles']) == 1
