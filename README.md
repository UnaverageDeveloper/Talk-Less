# Talk-Less

**An open-source, public-good news platform that makes bias visible, not hidden.**

Talk-Less uses a fully rule-based AI pipeline to present multi-perspective, source-grounded news summaries. No ads. No tracking. No editorial override. Just transparent, auditable news summarization.

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

## Core Principles

- **No monetization**: No ads, subscriptions, premium features, or sponsorships
- **No tracking**: No accounts, cookies, or personalization
- **No editorial override**: Fully automated, rule-based system
- **Open source**: AGPL v3 - inspect everything
- **Bias transparency**: Bias is documented and visible, not eliminated
- **Source grounding**: All summaries cite original sources
- **Auditable**: All decisions logged and reproducible

## What Makes Talk-Less Different?

### What We Don't Do
- ❌ Claim to be "unbiased" or "neutral"
- ❌ Rank stories by popularity or engagement
- ❌ Optimize for clicks, shares, or time-on-site
- ❌ Use proprietary algorithms or closed systems
- ❌ Track users or build profiles
- ❌ Monetize in any way

### What We Do
- ✅ Make our bias-handling rules transparent
- ✅ Present multiple perspectives when available
- ✅ Document detected bias in sources
- ✅ Link to original sources for verification
- ✅ Use transformative summaries (not republished content)
- ✅ Design for cost efficiency and portability
- ✅ Allow anyone to audit and reproduce our work

## How It Works

```
1. Fetch articles from configured news sources (rule-based selection)
2. Group articles covering the same story
3. Compare perspectives across sources
4. Generate transformative summaries with citations
5. Document detected bias patterns
6. Serve via simple API with aggressive caching
7. Display in minimal frontend with source links
```

**Everything is logged. Everything is auditable. Everything is open source.**

## Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design and technical details
- **[BIAS_HANDLING.md](BIAS_HANDLING.md)** - How we handle bias (plain English)
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute (BDFL governance)
- **[LICENSE](LICENSE)** - AGPL v3 license

## Project Status

🚧 **Early Development** - Building initial pipeline foundation

Current focus:
- Project structure and documentation
- Core pipeline components
- Source configuration system
- Initial bias detection rules

## Quick Start

```bash
# Clone repository
git clone https://github.com/UnaverageDeveloper/Talk-Less.git
cd Talk-Less

# Set up Python environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies (when available)
pip install -r requirements.txt

# Run pipeline (when implemented)
python -m backend.pipeline.run

# Start API server (when implemented)
python -m backend.api.server
```

## Technology Stack

- **Backend**: Python 3.11+, FastAPI, PostgreSQL, Redis
- **Pipeline**: Rule-based with LLM summarization (OpenAI/Anthropic APIs)
- **Frontend**: Vanilla JS or minimal framework
- **Infrastructure**: Docker, GitHub Actions

## Project Structure

```
Talk-Less/
├── backend/
│   ├── pipeline/         # News ingestion and summarization
│   ├── api/              # REST API
│   └── config/           # Configuration files
├── frontend/             # Static frontend
├── docs/                 # Additional documentation
├── tests/                # Test suite
├── ARCHITECTURE.md       # System design
├── BIAS_HANDLING.md      # Bias methodology
├── CONTRIBUTING.md       # Contribution guidelines
└── LICENSE               # AGPL v3
```

## Limitations

We are upfront about what we cannot do:

- **Not real-time**: Summaries update on schedule, not instantly
- **Not comprehensive**: Limited to configured sources
- **Not perfect**: Bias detection is rule-based and imperfect
- **Not personalized**: Everyone sees the same content
- **Not mobile-optimized**: Desktop-first design
- **Not monetizable**: By design, forever

See [BIAS_HANDLING.md](BIAS_HANDLING.md) for detailed discussion of limitations.

## Contributing

We welcome contributions that align with our core principles:

- Bug fixes and improvements
- New source adapters
- Better bias detection rules
- Documentation enhancements
- Security audits

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Not welcome**: Monetization features, tracking, personalization, closed-source components.

## License

This project is licensed under the **GNU Affero General Public License v3.0** (AGPL-3.0).

This means:
- You can use, modify, and distribute this code
- You must share your modifications under AGPL v3
- If you run modified code on a server, you must provide source to users
- No proprietary forks allowed

See [LICENSE](LICENSE) for full terms.

## Why AGPL v3?

We use AGPL v3 (not GPL v3) because:
- Talk-Less is designed to run as a network service
- AGPL requires sharing modifications even if not distributed
- This prevents proprietary forks that hide changes
- It ensures the community benefits from all improvements

## Philosophy

> "The answer to bias is not to pretend it doesn't exist. The answer is to make it visible, constrained, and auditable."

We believe:
- **Transparency** over claims of neutrality
- **Process** over individual judgment
- **Verifiability** over trust
- **Public good** over profit
- **Simplicity** over sophistication

## Non-Goals

Things we explicitly will NOT do:
- Grow at all costs
- Optimize for engagement
- Compete with commercial news
- Build a recommendation engine
- Create user accounts or profiles
- Monetize in any form
- Use proprietary technology

## Roadmap

Phase 1: Foundation (Current)
- ✅ Project structure and documentation
- ⏳ Core pipeline implementation
- ⏳ Source configuration system
- ⏳ Basic bias detection

Phase 2: MVP
- Backend API
- Minimal frontend
- Initial source set
- Caching layer

Phase 3: Refinement
- Improved bias detection
- More sources
- Better performance
- Public beta

See [GitHub Projects](https://github.com/UnaverageDeveloper/Talk-Less/projects) for detailed roadmap.

## Contact

- **Issues**: [GitHub Issues](https://github.com/UnaverageDeveloper/Talk-Less/issues)
- **Security**: See [CONTRIBUTING.md](CONTRIBUTING.md#security)
- **Questions**: Open an issue with `question` label

## Acknowledgments

This project is built on the shoulders of:
- Free software movement
- Open source community
- Researchers studying media bias
- Anyone who values transparency over profit

## Inspiration

Talk-Less is inspired by:
- Wikipedia's neutral point of view policy (but we admit we can't achieve it)
- Ad-free platforms like Library Genesis and Sci-Hub
- Public broadcasting's mission (minus government funding)
- Academic transparency and reproducibility standards

## Status Badges

- 🚧 **In Development**
- 📝 Documentation: Complete
- 🔧 Backend: In Progress
- 🎨 Frontend: Not Started
- 🧪 Testing: Not Started
- 🚀 Deployment: Not Started

---

**Talk-Less: Because news should inform, not manipulate.**
