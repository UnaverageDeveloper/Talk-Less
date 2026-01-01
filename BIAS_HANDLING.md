# Bias Handling in Talk-Less

## Core Philosophy

**Bias cannot be eliminated. It can only be constrained, documented, and made visible.**

Talk-Less does not claim to be "unbiased" or "neutral." Instead, it:
1. Makes its bias-handling rules transparent
2. Documents detected bias in sources
3. Presents multiple perspectives when available
4. Allows users to see the original sources

## What is Bias?

For Talk-Less, bias includes:
- **Selection bias**: Which stories get coverage
- **Framing bias**: How stories are presented
- **Source bias**: Who is quoted or cited
- **Emphasis bias**: What facts are highlighted
- **Omission bias**: What information is left out
- **Language bias**: Loaded words or emotional framing

## How Talk-Less Handles Bias

### 1. Source Selection

**Rule-Based Selection**
- Sources are configured in `sources.yaml`
- Selection criteria are transparent and versioned
- No manual curation of individual articles
- No ranking by traffic or popularity

**Diversity Requirements**
- Include sources across political spectrum
- Include local, national, and international outlets
- Include different media types (print, broadcast, online-native)
- Document each source's known leanings

**Example Configuration:**
```yaml
sources:
  - name: "Source A"
    url: "https://example.com/rss"
    documented_lean: "center-left"
    rationale: "Major outlet, fact-check record, editorial transparency"
  - name: "Source B"
    url: "https://example.org/rss"
    documented_lean: "center-right"
    rationale: "Major outlet, fact-check record, editorial transparency"
```

### 2. Bias Detection

**Automated Indicators**
Talk-Less detects and flags:
- Emotionally charged language (word lists)
- Lack of attributed sources ("sources say" vs named sources)
- One-sided framing (only quotes from one perspective)
- Unsupported claims (statements without evidence)

**Limitations**
- Detection is rule-based, not comprehensive
- Context can make flagged language appropriate
- Rules may have false positives
- New bias patterns emerge over time

### 3. Multi-Perspective Presentation

When multiple sources cover the same story:
- Compare framing across sources
- Identify unique facts or claims in each
- Note coverage gaps (who's not being quoted)
- Present summary that includes different angles

**Example:**
> **Story**: Policy announcement
> 
> **Perspective A** (Source 1, Source 2): Focuses on economic impact
> 
> **Perspective B** (Source 3): Focuses on social equity concerns
> 
> **Perspective C** (Source 4): Focuses on implementation challenges
>
> **Our Summary**: [Synthesizes all three perspectives with citations]

### 4. Transformative Summarization

Summaries are:
- **Original text**: Not excerpts from sources
- **Factually grounded**: All claims cited to sources
- **Multi-perspective**: Includes different viewpoints when present
- **Explicit about uncertainty**: Notes conflicting information

Summaries are NOT:
- Opinion or analysis
- Speculation about motives
- Predictions about outcomes
- Moral judgments

### 5. Transparency Indicators

Each summary includes:
- List of sources used (with links)
- Detected bias indicators per source
- Coverage gaps (perspectives not found)
- Confidence level in factual claims
- Last updated timestamp

## Our Own Biases

Talk-Less itself has biases built into its design:

### System Biases
1. **Tech bias**: Assumes access to internet and devices
2. **Language bias**: English-first (initially)
3. **Source bias**: Limited to configured sources
4. **Recency bias**: Recent stories over historical context
5. **Format bias**: Text-first over video/audio

### Design Biases
1. **Transparency bias**: Values openness over proprietary control
2. **Factual bias**: Values verifiable claims over speculation
3. **Attribution bias**: Values named sources over anonymous
4. **Diversity bias**: Values multiple perspectives over single narrative

### What We Don't Do
- We don't try to "balance" truth with falsehoods
- We don't equate all perspectives as equally valid
- We don't avoid calling out demonstrable falsehoods
- We don't hide corrections or mistakes

## Limitations

### What This System Cannot Do
- **Perfect objectivity**: Impossible by design
- **Real-time bias detection**: Rule-based systems lag reality
- **Context understanding**: Limited compared to human readers
- **Satirical intent**: May misclassify satire as biased
- **Cultural context**: Rules reflect current cultural understanding

### Known Weaknesses
- Source configuration requires human judgment
- Bias indicators may flag legitimate language
- Cannot detect all forms of subtle bias
- English-language focus limits scope
- Technical accessibility barriers

## Accountability

### How We Monitor Bias
- Public audit logs of source selection
- Version control of bias detection rules
- Regular review of false positives/negatives
- Community feedback (though not automated into system)

### How We Update
- Rules updated via pull requests
- Changes require documented rationale
- Testing before deployment
- Public changelog of rule modifications

### What We Don't Do
- Manual override of summaries
- Hide or bury controversial stories
- Optimize for user agreement or engagement
- A/B test different framings

## For Researchers & Critics

### Reproducibility
- All configuration is versioned
- Pipeline code is open source
- Logs are timestamped and structured
- Can replay pipeline with same inputs

### Audit Questions We Expect
1. How were sources chosen?
   - See `sources.yaml` with rationale
2. Why was Story X included but Story Y wasn't?
   - Check source RSS feeds at that time
3. Why does the summary frame it this way?
   - See prompt templates and LLM parameters
4. How is "bias" being defined?
   - See this document and detection rules

### Known Issues to Investigate
- Are our source choices themselves biased?
- Do our language rules reflect cultural biases?
- Are we over-correcting in any direction?
- What perspectives are systematically missing?

## Continuous Improvement

This document and our bias-handling approach will evolve:
- New bias patterns will be added to detection
- Source list will be reviewed periodically
- Rules will be refined based on real-world performance
- Community contributions will be considered (not auto-merged)

**However:**
- Core principles (transparency, multi-perspective, source grounding) won't change
- No individual can override the system
- All changes go through version control
- Everything remains open source

## Summary

Talk-Less makes bias **visible** rather than claiming to eliminate it. We:
1. Document our source selection criteria
2. Detect and flag bias indicators
3. Present multiple perspectives
4. Cite all sources
5. Make our rules public
6. Accept that we have our own biases
7. Invite scrutiny and criticism

**We are not perfect. We are transparent.**
