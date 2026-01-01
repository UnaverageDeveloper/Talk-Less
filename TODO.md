# TODO: Project Tasks

## High Priority

### License
- [ ] **Replace GPL v3 LICENSE with AGPL v3** 
  - Current LICENSE is GPL v3, needs to be AGPL v3
  - Download from: https://www.gnu.org/licenses/agpl-3.0.txt
  - Or copy from another AGPL v3 project
  - This is critical for the network service use case

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
- [ ] Implement embedding-based article grouping in `comparison.py`
- [ ] Implement LLM summarization in `summarization.py`
- [ ] Implement bias detection rules in `bias_detection.py`

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
