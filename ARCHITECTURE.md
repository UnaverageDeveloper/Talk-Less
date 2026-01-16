# Talk-Less Architecture

## Overview

Talk-Less is a fully open-source, rule-based AI-assisted news platform designed to present multi-perspective, bias-aware news summaries without ads, tracking, or editorial override.

## Core Principles

1. **No Monetization**: No ads, subscriptions, premium features, or sponsorships
2. **No User Tracking**: No accounts, no cookies, no personalization
3. **No Editorial Override**: Fully rule-based system; no human intervention in content
4. **Open Source**: AGPL v3 licensed; all code and rules are public
5. **Bias Transparency**: Bias is documented and visible, not hidden
6. **Source Grounding**: All summaries cite original sources
7. **Low Cost**: Designed for caching, batching, and infrastructure portability
8. **Auditability**: All decisions are logged and reproducible

## System Architecture

### High-Level Components

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│  (Static HTML/JS - No tracking, No personalization)         │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST
┌────────────────────────┴────────────────────────────────────┐
│                       Backend API                            │
│  (Flask/FastAPI - Read-only, Cached responses)              │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────┴────────────────────────────────────┐
│                    News Pipeline                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Ingestion  │→ │  Comparison  │→ │ Summarization│     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         ↓                  ↓                  ↓              │
│  ┌──────────────────────────────────────────────────┐      │
│  │         Configuration & Rules (YAML/JSON)        │      │
│  └──────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. News Pipeline

The pipeline is the core of Talk-Less, responsible for:
- **Source Selection**: Rule-based selection from configured news sources
- **Article Fetching**: Rate-limited, cached retrieval with robots.txt compliance
- **Multi-Perspective Comparison**: Identifying different angles on same stories
- **Transformative Summarization**: Creating original summaries (not excerpts)
- **Bias Documentation**: Detecting and documenting bias patterns
- **Source Attribution**: Maintaining links to original articles

#### Pipeline Stages

**Stage 1: Ingestion**
- Reads from RSS feeds and APIs based on configuration
- Rate limiting and caching to respect source servers
- Extracts article metadata and content
- Stores in normalized format

**Stage 2: Comparison**
- Groups articles by topic/event using embeddings
- Identifies perspective differences
- Detects coverage gaps across sources
- No ranking by popularity or emotion

**Stage 3: Summarization**
- Generates transformative summaries using LLMs
- Ensures all claims are cited to sources
- Documents detected bias patterns
- Produces output that is legally distinct from source material

### 2. Backend API

Simple REST API serving:
- `/summaries` - Get recent news summaries
- `/summary/{id}` - Get specific summary with sources
- `/sources` - List configured news sources
- `/transparency` - Audit logs and system metrics
- `/about` - System documentation

**Key Features:**
- Read-only (no POST/PUT/DELETE except admin endpoints)
- Aggressive caching (CDN-friendly)
- No session management
- No user-specific responses

### 3. Frontend

Minimal static site with:
- News summary display
- Source attribution UI
- Bias transparency indicators
- About/philosophy pages
- No JavaScript tracking
- No analytics
- No A/B testing

### 4. Configuration System

All behavior is controlled by configuration files:
- `sources.yaml` - News source definitions and rules
- `bias_indicators.yaml` - Bias detection patterns
- `pipeline_config.yaml` - Pipeline parameters
- `api_config.yaml` - API behavior

**Configuration is:**
- Version controlled
- Publicly visible
- Documented with rationale
- Changed through pull requests

### 5. Logging & Audit

Every decision is logged:
- Source selection rationale
- Articles fetched and when
- Summarization parameters used
- Detected bias patterns
- API requests (aggregated, not per-user)

Logs are:
- Structured (JSON)
- Timestamped
- Deterministic where possible
- Suitable for public transparency

## Data Flow

```
1. Scheduled trigger (cron) →
2. Pipeline reads sources.yaml →
3. Fetch articles from configured sources →
4. Group articles by topic →
5. Compare perspectives →
6. Generate summary with citations →
7. Document bias patterns →
8. Store in database with timestamps →
9. API serves cached summaries →
10. Frontend displays with source links
```

## Technology Stack

### Backend
- **Language**: Python 3.11+
- **Framework**: FastAPI (or Flask)
- **Database**: PostgreSQL (for summaries) + Redis (for cache)
- **LLM**: OpenAI/Anthropic APIs (configurable)
- **Task Queue**: Celery (for async pipeline)

### Frontend
- **Framework**: Vanilla JS or minimal framework (Svelte/Vue)
- **Build**: Vite or similar
- **Hosting**: Static file hosting (Netlify/Vercel/S3)

### Infrastructure
- **Deployment**: Docker + docker-compose
- **Monitoring**: Prometheus + Grafana (public metrics)
- **CI/CD**: GitHub Actions

## Security & Privacy

- No user authentication system
- No session cookies
- No tracking pixels
- No third-party analytics
- HTTPS only
- Rate limiting to prevent abuse
- Regular security audits (public results)

## Scalability

- Horizontal scaling via stateless API
- CDN caching for all GET endpoints
- Pipeline runs on schedule, not on-demand
- Database read replicas for high traffic
- Cost-optimized batch processing

## Limitations

- Summary freshness depends on pipeline schedule (not real-time)
- Limited to configured news sources
- Bias detection is rule-based, not perfect
- Summaries may miss nuances from original articles
- No personalization or recommendations
- No user feedback mechanism (by design)

## Future Considerations

- Multi-language support
- Historical archive
- API for researchers
- Public dataset exports
- Community-contributed source configurations (with review)

## Non-Goals

- Real-time breaking news
- User profiles or preferences
- Social features
- Mobile apps with notifications
- Engagement metrics
- Growth hacking
- Monetization strategy
