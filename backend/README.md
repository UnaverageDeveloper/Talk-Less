# Talk-Less Backend

This directory contains the backend components for Talk-Less.

## Structure

- `pipeline/` - News ingestion, comparison, and summarization pipeline
- `api/` - REST API for serving summaries
- `config/` - Configuration files (sources, bias rules, etc.)

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running

```bash
# Run pipeline
python -m backend.pipeline.run

# Start API server
python -m backend.api.server
```
