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
FastAPI Application for Talk-Less

This module provides the REST API for serving news summaries.
All endpoints are read-only (no POST/PUT/DELETE except admin).
No user tracking, no personalization, no authentication.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Talk-Less API",
    description="Open-source, public-good news platform API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware (open to all origins - no tracking)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Public API, no restrictions
    allow_credentials=False,  # No credentials needed
    allow_methods=["GET"],  # Read-only API
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """
    Root endpoint - provides API information.
    """
    return {
        "name": "Talk-Less API",
        "version": "0.1.0",
        "description": "Open-source, public-good news platform",
        "principles": [
            "No ads, no tracking, no personalization",
            "No editorial override - fully rule-based",
            "Bias made visible, not hidden",
            "All summaries cite sources",
            "Fully open source (AGPL v3)",
        ],
        "endpoints": {
            "/": "API information",
            "/summaries": "Get recent news summaries",
            "/summaries/{id}": "Get specific summary",
            "/sources": "List configured news sources",
            "/transparency": "System transparency data",
            "/about": "About the platform",
        },
        "documentation": "/docs",
    }


@app.get("/summaries")
async def get_summaries(
    limit: int = Query(default=20, ge=1, le=100, description="Number of summaries to return"),
    offset: int = Query(default=0, ge=0, description="Offset for pagination"),
):
    """
    Get recent news summaries.
    
    Returns list of summaries with:
    - Topic/headline
    - Summary text
    - List of sources
    - Detected bias indicators
    - Timestamp
    
    No personalization - everyone sees the same content.
    """
    logger.info(f"GET /summaries - limit={limit}, offset={offset}")
    
    # TODO: Implement actual database query
    # For now, return placeholder
    return {
        "summaries": [],
        "total": 0,
        "limit": limit,
        "offset": offset,
        "note": "Summaries not yet implemented - pipeline in development",
    }


@app.get("/summaries/{summary_id}")
async def get_summary(summary_id: str):
    """
    Get a specific summary by ID.
    
    Returns complete summary with:
    - Full summary text
    - All source articles with links
    - Perspective analysis
    - Bias indicators per source
    - Confidence level
    - Timestamp
    """
    logger.info(f"GET /summaries/{summary_id}")
    
    # TODO: Implement actual database query
    raise HTTPException(
        status_code=404,
        detail=f"Summary {summary_id} not found - implementation pending"
    )


@app.get("/sources")
async def get_sources():
    """
    List all configured news sources.
    
    Returns for each source:
    - Name and URL
    - Documented political lean (if known)
    - Fact-checking track record
    - Rationale for inclusion
    - Last fetch time
    
    Source selection is rule-based and transparent.
    """
    logger.info("GET /sources")
    
    # TODO: Load from configuration and add runtime stats
    return {
        "sources": [],
        "note": "Source list will be loaded from configuration",
        "selection_criteria": [
            "Editorial transparency",
            "Fact-checking track record",
            "Diverse perspectives",
            "Consistent publication",
            "RSS/API availability",
        ],
    }


@app.get("/transparency")
async def get_transparency():
    """
    Get transparency and audit data.
    
    Returns:
    - Pipeline execution stats
    - Bias detection summary
    - Source fetch history
    - System health metrics
    - Configuration version
    
    All data is aggregated - no individual user tracking.
    """
    logger.info("GET /transparency")
    
    return {
        "pipeline_stats": {
            "last_run": None,
            "articles_fetched": 0,
            "summaries_generated": 0,
            "bias_indicators_detected": 0,
        },
        "system_info": {
            "version": "0.1.0",
            "license": "AGPL v3",
            "source_code": "https://github.com/UnaverageDeveloper/Talk-Less",
        },
        "principles": {
            "no_tracking": True,
            "no_personalization": True,
            "no_monetization": True,
            "open_source": True,
        },
    }


@app.get("/about")
async def get_about():
    """
    Get information about the Talk-Less platform.
    
    Returns philosophy, architecture, and links to documentation.
    """
    logger.info("GET /about")
    
    return {
        "name": "Talk-Less",
        "tagline": "An open-source, public-good news platform that makes bias visible, not hidden",
        "philosophy": {
            "transparency": "Not just open source code, but open decision-making",
            "bias_handling": "Bias is documented and visible, not eliminated",
            "source_grounding": "All summaries cite original sources",
            "no_tracking": "No accounts, no cookies, no personalization",
            "no_monetization": "No ads, subscriptions, or premium features",
            "no_editorial_override": "Fully automated, rule-based system",
        },
        "documentation": {
            "readme": "https://github.com/UnaverageDeveloper/Talk-Less/blob/main/README.md",
            "architecture": "https://github.com/UnaverageDeveloper/Talk-Less/blob/main/ARCHITECTURE.md",
            "bias_handling": "https://github.com/UnaverageDeveloper/Talk-Less/blob/main/BIAS_HANDLING.md",
            "contributing": "https://github.com/UnaverageDeveloper/Talk-Less/blob/main/CONTRIBUTING.md",
        },
        "license": "AGPL v3",
        "repository": "https://github.com/UnaverageDeveloper/Talk-Less",
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
    }


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not found",
            "message": str(exc.detail) if hasattr(exc, 'detail') else "Resource not found",
        },
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An error occurred processing your request",
        },
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
