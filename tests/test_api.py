"""
Unit Tests for API Endpoints

Tests for the FastAPI application.
"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from api.server import app

# Create test client
client = TestClient(app)


class TestRootEndpoint:
    """Tests for root endpoint."""
    
    def test_root_returns_api_info(self):
        """Test that root endpoint returns API information."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data['name'] == "Talk-Less API"
        assert data['version'] == "0.1.0"
        assert 'principles' in data
        assert 'endpoints' in data
        assert 'documentation' in data
    
    def test_root_lists_principles(self):
        """Test that root endpoint lists core principles."""
        response = client.get("/")
        data = response.json()
        
        principles = data['principles']
        assert isinstance(principles, list)
        assert len(principles) > 0
        
        # Check for key principles
        principles_text = ' '.join(principles).lower()
        assert 'no tracking' in principles_text
        assert 'open source' in principles_text


class TestSummariesEndpoint:
    """Tests for summaries endpoint."""
    
    def test_get_summaries_returns_list(self):
        """Test that GET /summaries returns a list structure."""
        response = client.get("/summaries")
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'summaries' in data
        assert isinstance(data['summaries'], list)
        assert 'total' in data
        assert 'limit' in data
        assert 'offset' in data
    
    def test_get_summaries_respects_limit(self):
        """Test that limit parameter is respected."""
        response = client.get("/summaries?limit=10")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data['limit'] == 10
    
    def test_get_summaries_respects_offset(self):
        """Test that offset parameter is respected."""
        response = client.get("/summaries?offset=20")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data['offset'] == 20
    
    def test_get_summaries_validates_limit(self):
        """Test that limit parameter is validated."""
        # Too large limit should be rejected
        response = client.get("/summaries?limit=200")
        assert response.status_code == 422  # Validation error
        
        # Negative limit should be rejected
        response = client.get("/summaries?limit=-1")
        assert response.status_code == 422


class TestSummaryDetailEndpoint:
    """Tests for individual summary endpoint."""
    
    def test_get_summary_by_id_returns_404(self):
        """Test that non-existent summary returns 404."""
        response = client.get("/summaries/nonexistent")
        
        assert response.status_code == 404
        data = response.json()
        
        assert 'detail' in data


class TestSourcesEndpoint:
    """Tests for sources endpoint."""
    
    def test_get_sources_returns_structure(self):
        """Test that GET /sources returns proper structure."""
        response = client.get("/sources")
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'sources' in data
        assert isinstance(data['sources'], list)
        assert 'selection_criteria' in data
    
    def test_get_sources_lists_criteria(self):
        """Test that selection criteria are listed."""
        response = client.get("/sources")
        data = response.json()
        
        criteria = data['selection_criteria']
        assert isinstance(criteria, list)
        assert len(criteria) > 0


class TestTransparencyEndpoint:
    """Tests for transparency endpoint."""
    
    def test_get_transparency_returns_stats(self):
        """Test that GET /transparency returns transparency data."""
        response = client.get("/transparency")
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'pipeline_stats' in data
        assert 'system_info' in data
        assert 'principles' in data
    
    def test_transparency_confirms_no_tracking(self):
        """Test that transparency endpoint confirms no tracking."""
        response = client.get("/transparency")
        data = response.json()
        
        principles = data['principles']
        assert principles['no_tracking'] is True
        assert principles['no_personalization'] is True
        assert principles['no_monetization'] is True
        assert principles['open_source'] is True


class TestAboutEndpoint:
    """Tests for about endpoint."""
    
    def test_get_about_returns_info(self):
        """Test that GET /about returns platform information."""
        response = client.get("/about")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data['name'] == "Talk-Less"
        assert 'tagline' in data
        assert 'philosophy' in data
        assert 'documentation' in data
        assert 'license' in data
        assert 'repository' in data
    
    def test_about_describes_philosophy(self):
        """Test that about endpoint describes philosophy."""
        response = client.get("/about")
        data = response.json()
        
        philosophy = data['philosophy']
        assert 'transparency' in philosophy
        assert 'bias_handling' in philosophy
        assert 'no_tracking' in philosophy
        assert 'no_monetization' in philosophy


class TestHealthEndpoint:
    """Tests for health check endpoint."""
    
    def test_health_check_returns_healthy(self):
        """Test that health check returns healthy status."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data['status'] == "healthy"
        assert 'timestamp' in data


class TestCORSSettings:
    """Tests for CORS configuration."""
    
    def test_cors_allows_all_origins(self):
        """Test that CORS allows all origins (public API)."""
        response = client.get(
            "/",
            headers={"Origin": "https://example.com"}
        )
        
        assert response.status_code == 200
        # CORS headers should be present
        assert 'access-control-allow-origin' in response.headers


class TestAPIDesignPrinciples:
    """Tests to verify API adheres to design principles."""
    
    def test_no_post_endpoints_for_users(self):
        """Test that there are no POST endpoints for user data."""
        # Try to POST to various endpoints
        endpoints = ["/summaries", "/sources", "/about"]
        
        for endpoint in endpoints:
            response = client.post(endpoint, json={})
            # Should return 405 Method Not Allowed
            assert response.status_code == 405
    
    def test_no_authentication_required(self):
        """Test that no authentication is required for public endpoints."""
        endpoints = ["/", "/summaries", "/sources", "/transparency", "/about", "/health"]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            # Should not return 401 Unauthorized
            assert response.status_code != 401
