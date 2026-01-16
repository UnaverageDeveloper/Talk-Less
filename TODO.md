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
- [ ] Create FastAPI application
- [ ] Implement REST endpoints
- [ ] Add caching layer
- [ ] Set up database models

#### Frontend
- [ ] Set up frontend framework
- [ ] Create summary display UI
- [ ] Implement source attribution display
- [ ] Add bias transparency indicators

#### Testing
- [ ] Write unit tests for pipeline components
- [ ] Write integration tests
- [ ] Add test fixtures
- [ ] Set up CI/CD

## Medium Priority

- [ ] Set up PostgreSQL schema
- [ ] Configure Redis caching
- [ ] Implement Celery task queue
- [ ] Add monitoring and metrics
- [ ] Create deployment configuration
- [ ] Write API documentation
- [ ] Add more comprehensive logging

## Low Priority

- [ ] Multi-language support
- [ ] Historical archive
- [ ] Public API for researchers
- [ ] Community contribution system

## Documentation Needed

- [ ] API documentation
- [ ] Deployment guide
- [ ] Development guide
- [ ] Source selection rationale document
- [ ] Limitations and known issues document
