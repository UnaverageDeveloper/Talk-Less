"""
Integration Tests for Talk-Less Pipeline

End-to-end tests for the complete AI-powered news processing pipeline.
Tests the full flow: ingestion → grouping → summarization → bias detection.
"""

import pytest
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock

# Add backend to path
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from pipeline.ingestion import Article, ArticleIngester
from pipeline.comparison import ArticleGroup, ArticleComparer
from pipeline.summarization import Summary, ArticleSummarizer
from pipeline.bias_detection import BiasIndicator, BiasDetector


@pytest.fixture
def sample_articles():
    """Create sample articles for testing."""
    now = datetime.now()
    return [
        Article(
            title="Climate Summit Reaches Historic Agreement",
            url="https://source1.com/climate-1",
            source="Source 1",
            published_at=now - timedelta(hours=2),
            content="World leaders at the climate summit announced a historic agreement to reduce carbon emissions by 50% by 2030. The deal includes commitments from over 150 countries.",
            author="Reporter A",
        ),
        Article(
            title="Major Climate Deal Signed at International Summit",
            url="https://source2.com/climate-2",
            source="Source 2",
            published_at=now - timedelta(hours=1),
            content="An unprecedented climate agreement was reached today with nations pledging significant emission reductions. Critics question implementation details.",
            author="Reporter B",
        ),
        Article(
            title="Tech Giant Announces AI Breakthrough",
            url="https://source1.com/tech-1",
            source="Source 1",
            published_at=now - timedelta(minutes=30),
            content="A leading technology company revealed a new artificial intelligence system that can process natural language with human-level comprehension.",
            author="Tech Reporter",
        ),
    ]


@pytest.fixture
def config_dict():
    """Configuration dictionary for testing."""
    return {
        'comparison': {
            'min_articles_per_group': 2,
            'similarity_threshold': 0.5,
            'max_articles_per_group': 10,
        },
        'summarization': {
            'model': 'gpt-3.5-turbo',
            'temperature': 0.3,
            'max_summary_length': 500,
            'min_summary_length': 100,
            'require_citations': True,
            'max_retries': 2,
        },
        'bias_detection': {
            'enabled': True,
            'min_confidence': 'low',
            'generate_reports': True,
        },
    }


class TestPipelineIntegration:
    """Integration tests for complete pipeline flow."""

    @pytest.mark.integration
    def test_article_grouping_integration(self, sample_articles, config_dict):
        """Test that articles are correctly grouped by topic."""
        comparer = ArticleComparer(config_dict)
        
        # Group articles
        groups = comparer.group_articles(sample_articles)
        
        # Should create at least one group (climate articles)
        assert len(groups) >= 1
        
        # Check that climate articles are grouped together
        climate_group = None
        for group in groups:
            titles = [a.title for a in group.articles]
            if "Climate" in str(titles):
                climate_group = group
                break
        
        assert climate_group is not None
        assert len(climate_group.articles) == 2
        assert climate_group.source_count == 2
    
    @pytest.mark.integration
    def test_bias_detection_integration(self, sample_articles, config_dict):
        """Test bias detection on real article content."""
        # Load bias indicators from config
        bias_config = {
            'indicators': {
                'loaded_language': {
                    'patterns': ['historic', 'unprecedented', 'major'],
                    'severity': 'low',
                },
            }
        }
        
        detector = BiasDetector(config_dict)
        
        # Detect bias in articles
        for article in sample_articles:
            indicators = detector.detect_bias(article, bias_config)
            
            # Climate articles should have some bias indicators
            if "Climate" in article.title:
                assert len(indicators) > 0
                assert any(i.indicator_type == "loaded_language" for i in indicators)
    
    @pytest.mark.integration
    @pytest.mark.slow
    @patch('openai.OpenAI')
    def test_summarization_integration(self, mock_openai, sample_articles, config_dict):
        """Test LLM summarization with mocked API."""
        # Mock OpenAI response
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = (
            "World leaders reached a climate agreement to reduce emissions by 50% by 2030 [Source: Source 1]. "
            "Over 150 countries committed to the deal [Source: Source 1]. Critics question implementation [Source: Source 2]. "
            "This represents an unprecedented international cooperation [Source: Source 2]."
        )
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        summarizer = ArticleSummarizer(config_dict)
        
        # Create article group
        comparer = ArticleComparer(config_dict)
        groups = comparer.group_articles(sample_articles)
        
        if len(groups) > 0:
            group = groups[0]
            
            # Generate summary
            summary = summarizer.generate_summary(group)
            
            assert summary is not None
            assert len(summary.text) > 0
            assert summary.article_count == len(group.articles)
            assert len(summary.source_citations) > 0
            assert summary.transformative is True
    
    @pytest.mark.integration
    def test_end_to_end_pipeline_flow(self, sample_articles, config_dict):
        """Test complete pipeline from articles to final output."""
        # Step 1: Group articles
        comparer = ArticleComparer(config_dict)
        groups = comparer.group_articles(sample_articles)
        
        assert len(groups) > 0
        
        # Step 2: Detect bias
        bias_config = {
            'indicators': {
                'loaded_language': {
                    'patterns': ['historic', 'unprecedented'],
                    'severity': 'low',
                }
            }
        }
        detector = BiasDetector(config_dict)
        
        all_indicators = []
        for article in sample_articles:
            indicators = detector.detect_bias(article, bias_config)
            all_indicators.extend(indicators)
        
        # Should detect some bias
        assert len(all_indicators) > 0
        
        # Step 3: Verify group metadata
        for group in groups:
            assert group.group_id is not None
            assert group.article_count > 0
            assert group.source_count > 0
            assert len(group.articles) > 0


class TestPipelineValidation:
    """Tests for validating pipeline output quality."""
    
    @pytest.mark.integration
    def test_summary_transformative_validation(self):
        """Test that summaries are transformative, not copied."""
        original_text = "The quick brown fox jumps over the lazy dog repeatedly."
        summary_text = "A brown fox jumped over a dog."
        
        # Check for long copied sequences
        def has_copied_text(original, summary, min_length=10):
            words_orig = original.lower().split()
            words_summ = summary.lower().split()
            
            for i in range(len(words_summ) - min_length + 1):
                sequence = ' '.join(words_summ[i:i+min_length])
                if sequence in original.lower():
                    return True
            return False
        
        # This should be transformative
        assert not has_copied_text(original_text, summary_text)
        
        # This should be detected as copied
        copied_summary = "The quick brown fox jumps over the lazy dog"
        assert has_copied_text(original_text, copied_summary)
    
    @pytest.mark.integration
    def test_citation_validation(self):
        """Test that summaries contain proper citations."""
        summary_text = (
            "The agreement includes emission reductions [Source: Source 1]. "
            "Implementation details are unclear [Source: Source 2]."
        )
        
        # Extract citations
        import re
        citations = re.findall(r'\[Source: ([^\]]+)\]', summary_text)
        
        assert len(citations) >= 2
        assert "Source 1" in citations
        assert "Source 2" in citations
    
    @pytest.mark.integration
    def test_multiple_perspectives_validation(self, sample_articles):
        """Test that article groups contain multiple perspectives."""
        config = {
            'comparison': {
                'min_articles_per_group': 2,
                'similarity_threshold': 0.5,
                'max_articles_per_group': 10,
            }
        }
        
        comparer = ArticleComparer(config)
        groups = comparer.group_articles(sample_articles)
        
        for group in groups:
            if group.article_count >= 2:
                # Should have articles from different sources
                sources = set(a.source for a in group.articles)
                assert len(sources) >= 2, "Group should have multiple source perspectives"


class TestPipelineErrorHandling:
    """Tests for pipeline error handling and resilience."""
    
    @pytest.mark.integration
    def test_empty_article_list(self, config_dict):
        """Test pipeline handles empty article list gracefully."""
        comparer = ArticleComparer(config_dict)
        groups = comparer.group_articles([])
        
        assert groups == []
    
    @pytest.mark.integration
    def test_single_article(self, config_dict):
        """Test pipeline handles single article."""
        article = Article(
            title="Single Article",
            url="https://example.com/single",
            source="Test Source",
            published_at=datetime.now(),
            content="Single article content for testing.",
            author="Author",
        )
        
        comparer = ArticleComparer(config_dict)
        groups = comparer.group_articles([article])
        
        # Single article might be grouped alone or not grouped
        assert isinstance(groups, list)
    
    @pytest.mark.integration
    def test_malformed_article_content(self, config_dict):
        """Test pipeline handles malformed content."""
        article = Article(
            title="",  # Empty title
            url="https://example.com/malformed",
            source="Test Source",
            published_at=datetime.now(),
            content="",  # Empty content
            author=None,  # No author
        )
        
        detector = BiasDetector(config_dict)
        bias_config = {'indicators': {}}
        
        # Should not crash
        indicators = detector.detect_bias(article, bias_config)
        assert isinstance(indicators, list)


class TestPipelinePerformance:
    """Tests for pipeline performance characteristics."""
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_large_article_set_performance(self, config_dict):
        """Test pipeline performance with larger article set."""
        import time
        
        # Create 50 articles
        articles = []
        now = datetime.now()
        for i in range(50):
            articles.append(Article(
                title=f"Article {i} about topic {i % 5}",
                url=f"https://example.com/article-{i}",
                source=f"Source {i % 10}",
                published_at=now - timedelta(hours=i),
                content=f"Content for article {i} discussing topic {i % 5}.",
                author=f"Author {i}",
            ))
        
        comparer = ArticleComparer(config_dict)
        
        start = time.time()
        groups = comparer.group_articles(articles)
        duration = time.time() - start
        
        # Should complete in reasonable time (< 30 seconds for 50 articles)
        assert duration < 30
        assert len(groups) > 0
    
    @pytest.mark.integration
    def test_memory_efficiency(self, sample_articles, config_dict):
        """Test that pipeline doesn't create excessive object copies."""
        comparer = ArticleComparer(config_dict)
        groups = comparer.group_articles(sample_articles)
        
        # Articles in groups should reference same objects, not copies
        for group in groups:
            for article in group.articles:
                assert any(article is orig for orig in sample_articles), \
                    "Articles should be references, not copies"


class TestPipelinePrinciples:
    """Tests verifying core Talk-Less principles."""
    
    @pytest.mark.integration
    def test_no_tracking_in_pipeline(self, sample_articles, config_dict):
        """Verify pipeline doesn't track user behavior."""
        # Pipeline components should not have tracking attributes
        comparer = ArticleComparer(config_dict)
        detector = BiasDetector(config_dict)
        
        # Check no user/session tracking attributes
        assert not hasattr(comparer, 'user_id')
        assert not hasattr(comparer, 'session_id')
        assert not hasattr(detector, 'user_id')
        assert not hasattr(detector, 'session_id')
    
    @pytest.mark.integration
    def test_deterministic_behavior(self, sample_articles, config_dict):
        """Test that pipeline produces consistent results."""
        comparer = ArticleComparer(config_dict)
        
        # Run twice with same input
        groups1 = comparer.group_articles(sample_articles)
        groups2 = comparer.group_articles(sample_articles)
        
        # Should produce same number of groups
        assert len(groups1) == len(groups2)
        
        # Group IDs should be deterministic
        ids1 = sorted([g.group_id for g in groups1])
        ids2 = sorted([g.group_id for g in groups2])
        assert ids1 == ids2
    
    @pytest.mark.integration
    def test_transparent_bias_detection(self, sample_articles, config_dict):
        """Test that bias detection is transparent and auditable."""
        bias_config = {
            'indicators': {
                'loaded_language': {
                    'patterns': ['historic', 'unprecedented'],
                    'severity': 'low',
                    'description': 'Emotionally charged language',
                }
            }
        }
        
        detector = BiasDetector(config_dict)
        
        for article in sample_articles:
            indicators = detector.detect_bias(article, bias_config)
            
            # Each indicator should have transparent metadata
            for indicator in indicators:
                assert indicator.indicator_type is not None
                assert indicator.confidence is not None
                assert indicator.context is not None
                # Can trace back to detection rule
                assert indicator.indicator_type in bias_config['indicators']
