# Contributing to Talk-Less

## Governance Model

Talk-Less uses a **Benevolent Dictator For Life (BDFL)** governance model with strong constraints.

### Core Principles (Non-Negotiable)

These principles cannot be changed:
1. ✓ No monetization (ads, subscriptions, sponsorships)
2. ✓ No user tracking or personalization
3. ✓ No editorial override of automated system
4. ✓ AGPL v3 license
5. ✓ Public source code and configuration
6. ✓ Bias transparency over bias elimination
7. ✓ Source grounding for all claims

Any contribution that violates these principles will be rejected.

### Decision Authority

The project maintainer has final authority on:
- Which contributions to accept
- Source selection criteria
- Bias detection rules
- Technical architecture decisions
- Release timing

**However:**
- All decisions must be documented with rationale
- All code and configuration remains open source
- Community can fork if they disagree
- No secret rules or configurations

## How to Contribute

### Types of Contributions Welcome

1. **Bug fixes**
   - Pipeline errors
   - API issues
   - Frontend bugs
   - Documentation corrections

2. **New features** (if aligned with principles)
   - New source adapters
   - Improved bias detection rules
   - Better summarization prompts
   - Performance optimizations

3. **Documentation**
   - Clarifications
   - Examples
   - Translations
   - Architecture explanations

4. **Testing**
   - Unit tests
   - Integration tests
   - Load testing
   - Security audits

5. **Research**
   - Bias analysis
   - Source diversity studies
   - Accessibility reviews
   - Performance benchmarks

### Types of Contributions NOT Welcome

- Monetization features (ads, paywalls, donations)
- User tracking or analytics
- Personalization or recommendations
- Engagement optimization
- Closed-source components
- Proprietary service dependencies
- Growth hacking features

## Contribution Process

### 1. Before You Start

- Check existing issues and PRs
- Review [ARCHITECTURE.md](ARCHITECTURE.md) and [BIAS_HANDLING.md](BIAS_HANDLING.md)
- For large changes, open an issue first to discuss
- Ensure your change aligns with core principles

### 2. Development Setup

```bash
# Clone the repository
git clone https://github.com/UnaverageDeveloper/Talk-Less.git
cd Talk-Less

# Set up Python environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest

# Run linters
black .
flake8 .
mypy .
```

### 3. Making Changes

- Create a feature branch: `git checkout -b feature/your-feature-name`
- Write clean, documented code
- Follow existing code style
- Add tests for new functionality
- Update documentation if needed
- Keep commits focused and atomic

### 4. Code Standards

**Python:**
- Follow PEP 8
- Use type hints
- Write docstrings for public functions
- Keep functions small and focused
- Prefer clarity over cleverness

**JavaScript:**
- Use modern ES6+ syntax
- Avoid external dependencies when possible
- No tracking or analytics code
- Comment non-obvious logic

**Configuration:**
- YAML for human-edited files
- JSON for machine-generated data
- Always include rationale for rules
- Version control all configuration

### 5. Testing

All contributions must include tests:
- Unit tests for new functions
- Integration tests for pipeline changes
- No reduction in code coverage
- Tests must be deterministic

### 6. Documentation

Update documentation for:
- New features or changes
- Configuration options
- API endpoints
- Known limitations
- Bias implications

### 7. Submitting Pull Request

**PR Description Should Include:**
- What problem does this solve?
- How does it work?
- Are there any trade-offs?
- Does it affect bias handling?
- Are there new dependencies?
- Is documentation updated?

**PR Checklist:**
- [ ] Code follows project style
- [ ] Tests added and passing
- [ ] Documentation updated
- [ ] No violations of core principles
- [ ] Rationale provided for rule changes
- [ ] No secrets or credentials in code

### 8. Review Process

1. Automated checks (tests, linting) must pass
2. Maintainer reviews code and rationale
3. Discussion and iteration if needed
4. Approval and merge, or rejection with explanation
5. Merged code becomes AGPL v3 licensed

**Expected Review Time:**
- Bug fixes: 1-3 days
- Small features: 1 week
- Large features: 2-4 weeks
- Rule changes: Requires more discussion

## Source Configuration Changes

Adding or modifying news sources requires:

1. **Source Information**
   - Name and URL
   - RSS/API endpoint
   - Documented political lean (if known)
   - Fact-checking track record
   - Editorial transparency

2. **Rationale**
   - Why include this source?
   - What perspective does it add?
   - How does it improve diversity?
   - Are there quality concerns?

3. **Testing**
   - Verify RSS/API works
   - Test rate limiting
   - Check robots.txt compliance
   - Validate content extraction

## Bias Detection Rule Changes

Modifying bias detection rules requires:

1. **Rule Definition**
   - Pattern or keyword
   - What bias does it indicate?
   - Confidence level

2. **Justification**
   - Why is this biased language?
   - Are there false positive risks?
   - How common is this pattern?

3. **Testing**
   - Examples of true positives
   - Examples of false positives
   - Impact on existing summaries

## Security

### Reporting Vulnerabilities

**DO NOT** open public issues for security vulnerabilities.

Instead:
1. Email security details to project maintainer
2. Allow reasonable time for fix (90 days)
3. Coordinated disclosure after fix

We commit to:
- Acknowledging report within 48 hours
- Regular updates on fix progress
- Public disclosure after fix deployed
- Credit to reporter (if desired)

### Security Scope

In scope:
- Code injection vulnerabilities
- Data leakage risks
- DoS attack vectors
- Dependency vulnerabilities
- Infrastructure security

Out of scope:
- Social engineering
- Physical security
- Brute force attacks (rate limiting handles this)

## Code of Conduct

### Expected Behavior

- Be respectful and constructive
- Assume good faith
- Focus on ideas, not people
- Accept constructive criticism
- Acknowledge different perspectives

### Unacceptable Behavior

- Personal attacks or harassment
- Trolling or inflammatory comments
- Publishing others' private information
- Sustained disruption
- Violation of core principles

### Enforcement

1. Warning for first offense
2. Temporary ban for repeated issues
3. Permanent ban for severe or continued violations

Maintainer has final say on enforcement.

## Licensing

By contributing, you agree that:
- Your contributions will be licensed under AGPL v3
- You have the right to submit your contribution
- You understand AGPL v3 requirements

If you want to contribute but can't agree to AGPL v3, please don't submit.

## Questions?

- Open an issue for questions
- Tag it with `question` label
- Be specific about what you need clarification on
- Review docs first to avoid duplicate questions

## Fork Policy

You are welcome to fork Talk-Less:
- All code is AGPL v3 licensed
- Must maintain AGPL v3 in fork
- Must provide source code to users
- Must maintain license headers
- Can modify freely within license terms

We encourage forks to:
- Experiment with different approaches
- Serve different communities
- Test controversial changes

## Roadmap

See [GitHub Projects](https://github.com/UnaverageDeveloper/Talk-Less/projects) for:
- Planned features
- Current priorities
- Known issues

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Credited in release notes
- Acknowledged in documentation

We don't offer:
- Monetary compensation
- Swag or merchandise
- Exclusive access or features

## Summary

Contributing to Talk-Less means:
1. Respecting core principles
2. Being transparent about changes
3. Accepting AGPL v3 terms
4. Prioritizing trust over growth
5. Making bias visible, not hidden

**Thank you for helping build a trustworthy, open news platform.**
