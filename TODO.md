# TODO: Project Tasks

## High Priority

### License
- [x] **Replace GPL v3 LICENSE with AGPL v3** ✅ COMPLETE
  - LICENSE file replaced with AGPL v3
  - README.md updated to mention AGPL v3
  - CONTRIBUTING.md references AGPL v3
  - setup.py metadata updated
  - License headers added to all source files
  - This ensures transparency for network service use case

### Implementation

#### Pipeline Components
- [x] **Implement actual RSS/API fetching in `ingestion.py`** ✅ COMPLETE
  - RSS feed parsing with feedparser
  - API endpoint support
  - Content extraction and normalization
  - Age filtering
- [x] **Implement rate limiting** ✅ COMPLETE
  - Per-source rate limiter
  - Configurable requests per minute
  - Automatic waiting between requests
- [x] **Implement caching layer** ✅ COMPLETE
  - Redis-based distributed cache
  - Graceful degradation if Redis unavailable
  - Configurable TTL
  - Cache key generation
- [x] **Implement embedding-based article grouping in `comparison.py`** ✅ COMPLETE
  - Sentence transformer embeddings (all-MiniLM-L6-v2)
  - DBSCAN clustering algorithm
  - Perspective analysis
  - Coverage gap detection
- [x] **Implement LLM summarization in `summarization.py`** ✅ COMPLETE
  - OpenAI (GPT-4) and Anthropic (Claude) integration
  - Transformative summary generation with citations
  - Summary validation (length, citations, distinctness)
  - Retry logic for failed generations
- [x] **Implement bias detection rules in `bias_detection.py`** ✅ COMPLETE
  - Rule-based detection engine
  - Loaded language detection
  - Attribution quality checking
  - Framing analysis
  - Transparency reporting

#### Configuration
- [ ] Add real news sources to `sources.yaml` (requires research)
- [ ] Expand bias detection patterns in `bias_indicators.yaml`
- [ ] Configure database connection strings

#### Backend API
- [x] **Create FastAPI application** ✅ COMPLETE
- [x] **Implement REST endpoints** ✅ COMPLETE (6 endpoints)
- [x] **Add caching layer** ✅ COMPLETE
- [x] **Set up database models** ✅ COMPLETE (4 models)

#### Frontend
- [ ] Set up frontend framework
- [ ] Create summary display UI
- [ ] Implement source attribution display
- [ ] Add bias transparency indicators

#### Testing
- [x] **Write unit tests for pipeline components** ✅ COMPLETE
  - 170+ unit tests for all components
  - Article, ArticleIngester, ArticleComparer tests
  - ArticleSummarizer, BiasDetector tests
  - API endpoint tests
- [x] **Write integration tests** ✅ COMPLETE
  - End-to-end pipeline flow tests
  - Quality validation tests (transformative, citations)
  - Performance tests (large datasets)
  - Error handling tests
  - Principles validation tests
- [x] **Add test fixtures** ✅ COMPLETE
  - Sample articles fixture
  - Configuration fixture
  - Mocked API responses
- [x] **Set up CI/CD** ✅ COMPLETE (Phase 7)

#### Deployment & Infrastructure
- [x] **Create Docker infrastructure** ✅ COMPLETE (Phase 7)
  - Production Dockerfile
  - docker-compose.yml with all services
  - Environment configuration (.env.example)
  - .dockerignore optimization
- [x] **Set up CI/CD pipeline** ✅ COMPLETE (Phase 7)
  - GitHub Actions workflow
  - Automated testing (lint, test, security)
  - License compliance checks
  - Docker build validation
  - Transparency reporting
- [x] **Write deployment guides** ✅ COMPLETE (Phase 7)
  - DEPLOYMENT.md - Production deployment guide
  - PHASE7_DEPLOYMENT.md - Implementation details
  - Quick start instructions
  - Security hardening guide
  - Monitoring and troubleshooting

## Medium Priority

- [ ] Set up PostgreSQL schema (structure exists, needs initialization)
- [x] Configure Redis caching ✅ COMPLETE
- [ ] Implement Celery task queue (optional enhancement)
- [ ] Add monitoring and metrics (guidance provided in DEPLOYMENT.md)
- [x] Create deployment configuration ✅ COMPLETE
- [x] Write API documentation ✅ COMPLETE
- [x] Add comprehensive logging ✅ COMPLETE

## Low Priority

- [ ] Multi-language support
- [ ] Historical archive
- [ ] Public API for researchers
- [ ] Community contribution system

## Documentation Status

- [x] **API documentation** ✅ COMPLETE (backend/api/README.md)
- [x] **Deployment guide** ✅ COMPLETE (DEPLOYMENT.md)
- [x] **Development guide** ✅ COMPLETE (QUICKSTART.md, CONTRIBUTING.md)
- [x] **Testing guide** ✅ COMPLETE (PHASE6_TESTING.md)
- [x] **Infrastructure guide** ✅ COMPLETE (PHASE7_DEPLOYMENT.md)
- [x] **Implementation guides** ✅ COMPLETE (PHASE2, PHASE3 docs)
- [ ] Source selection rationale document (partially in BIAS_HANDLING.md)
- [ ] Limitations and known issues document (partially in README.md)
