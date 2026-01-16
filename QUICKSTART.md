# Developer Quick Start Guide

This guide will help you get started with Talk-Less development.

## Prerequisites

- Python 3.11 or higher
- Git
- Basic understanding of news aggregation and NLP concepts

## Initial Setup

### 1. Clone the Repository

```bash
git clone https://github.com/UnaverageDeveloper/Talk-Less.git
cd Talk-Less
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Understand the Project Structure

```
Talk-Less/
├── backend/
│   ├── pipeline/      # Core news processing pipeline
│   ├── api/          # REST API (to be implemented)
│   └── config/       # Configuration files (YAML)
├── frontend/         # Frontend application (to be implemented)
├── tests/           # Test suite (to be implemented)
└── docs/            # Additional documentation
```

### 4. Read the Documentation

Before coding, read:
1. [README.md](README.md) - Project overview and philosophy
2. [ARCHITECTURE.md](ARCHITECTURE.md) - System design
3. [BIAS_HANDLING.md](BIAS_HANDLING.md) - Bias methodology
4. [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines

## Running the Pipeline

The pipeline is currently a stub with basic structure:

```bash
# Run the pipeline
python backend/pipeline/run.py
```

Expected output: The pipeline will run but won't fetch articles yet (implementation pending).

## Development Workflow

### 1. Pick a Task

Check [TODO.md](TODO.md) for tasks to work on.

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 3. Make Changes

- Write clean, documented code
- Follow existing code style
- Add type hints
- Keep functions small and focused

### 4. Test Your Changes

```bash
# Run tests (when available)
pytest

# Check code style
black backend/
flake8 backend/
mypy backend/
```

### 5. Commit and Push

```bash
git add .
git commit -m "Description of your changes"
git push origin feature/your-feature-name
```

### 6. Open Pull Request

- Provide clear description
- Explain rationale
- Reference any related issues

## Configuration Files

All behavior is controlled by YAML files in `backend/config/`:

- **sources.yaml** - News sources and selection rules
- **bias_indicators.yaml** - Bias detection patterns
- **pipeline_config.yaml** - Pipeline settings

Changes to configuration files must include rationale.

## Key Principles to Remember

1. **No tracking or personalization** - Everyone sees the same content
2. **No monetization** - No ads, subscriptions, or paid features
3. **Transparency first** - All decisions must be auditable
4. **Source grounding** - All claims must cite sources
5. **Bias visibility** - Make bias visible, don't claim to eliminate it

## Current Implementation Status

✅ **Done:**
- Project structure
- Documentation
- Configuration system
- Pipeline component stubs

🚧 **In Progress:**
- Nothing currently

⏳ **To Do:**
- Implement RSS/API fetching
- Implement article grouping
- Implement LLM summarization
- Implement bias detection
- Create backend API
- Build frontend
- Add tests

## Common Tasks

### Adding a News Source

1. Edit `backend/config/sources.yaml`
2. Add source with all required fields
3. Include rationale for adding
4. Document political lean (if known)
5. Test that RSS/API works

### Adding a Bias Indicator

1. Edit `backend/config/bias_indicators.yaml`
2. Define pattern or keyword
3. Provide rationale
4. Test for false positives
5. Document confidence level

### Implementing Pipeline Components

Each component in `backend/pipeline/` has TODOs:

- `ingestion.py` - Implement RSS/API fetching
- `comparison.py` - Implement article grouping
- `summarization.py` - Implement LLM calls
- `bias_detection.py` - Implement detection rules

## Testing

Currently no tests exist. To add tests:

1. Create test files in `tests/` directory
2. Follow pytest conventions
3. Test both success and failure cases
4. Mock external dependencies
5. Ensure tests are deterministic

## Getting Help

- Open an issue with the `question` label
- Tag with relevant component (pipeline, api, frontend)
- Be specific about what you need help with
- Review existing docs first

## Code Style

- **Python**: PEP 8, type hints, docstrings
- **YAML**: 2-space indentation, comments for rationale
- **Markdown**: Clear headings, code blocks for examples

## Security

- Never commit secrets or credentials
- Use environment variables for sensitive data
- Report security issues privately (see CONTRIBUTING.md)

## License

All contributions are AGPL v3 licensed. By contributing, you agree to this license.

## Questions?

If you're stuck or confused:
1. Re-read the relevant documentation
2. Check TODO.md for context
3. Look at existing code for patterns
4. Open an issue if still unclear

**Welcome to Talk-Less! Let's build something trustworthy.**
