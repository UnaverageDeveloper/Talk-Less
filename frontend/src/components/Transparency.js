/*
 * Talk-Less Transparency Page Component
 * Copyright (C) 2024 Talk-Less Contributors
 * Licensed under AGPL-3.0-or-later
 */

import React from 'react';
import { Link } from 'react-router-dom';
import './Transparency.css';

function Transparency() {
  return (
    <div className="transparency-page">
      <div className="page-header">
        <h1>Transparency Report</h1>
        <p className="page-subtitle">
          Complete transparency about our methods, algorithms, and limitations
        </p>
      </div>

      <section className="transparency-section card">
        <h2>Overview</h2>
        <p>
          This page documents everything about how Talk-Less works. We believe
          transparency is essential for any platform that aggregates and summarizes
          news content.
        </p>
      </section>

      <section className="transparency-section card">
        <h2>Technical Architecture</h2>
        
        <h3>Pipeline Components</h3>
        <dl className="definition-list">
          <dt>Article Ingestion</dt>
          <dd>
            Articles are collected via RSS feeds and public APIs. We fetch metadata
            (title, URL, publish date, source) and content. No paywalled content
            is accessed.
          </dd>

          <dt>Clustering Algorithm</dt>
          <dd>
            We use DBSCAN clustering with sentence transformer embeddings
            (all-MiniLM-L6-v2) to group articles about the same topic. This is
            a standard unsupervised learning approach.
          </dd>

          <dt>Perspective Analysis</dt>
          <dd>
            Within each cluster, we identify different perspectives by analyzing
            semantic differences between articles. This helps ensure diverse
            viewpoint representation.
          </dd>

          <dt>Summary Generation</dt>
          <dd>
            Summaries are generated using large language models (GPT-4 or Claude)
            with specific prompts emphasizing multi-perspective synthesis and
            citation requirements.
          </dd>

          <dt>Bias Detection</dt>
          <dd>
            Rule-based system checks for loaded language, unsupported claims,
            attribution quality, and framing issues. Results are displayed
            transparently.
          </dd>
        </dl>
      </section>

      <section className="transparency-section card">
        <h2>Source Selection Criteria</h2>
        
        <p>News sources are evaluated on:</p>
        
        <div className="criteria-grid">
          <div className="criteria-item">
            <h4>Editorial Independence</h4>
            <p>
              Sources must demonstrate independence from political parties,
              governments, or corporate interests that compromise editorial
              judgment.
            </p>
          </div>

          <div className="criteria-item">
            <h4>Fact-Checking Standards</h4>
            <p>
              Must have published corrections policies and demonstrated
              commitment to factual accuracy.
            </p>
          </div>

          <div className="criteria-item">
            <h4>Source Attribution</h4>
            <p>
              Articles must clearly cite sources for claims and distinguish
              between reporting and opinion.
            </p>
          </div>

          <div className="criteria-item">
            <h4>Ideological Diversity</h4>
            <p>
              We intentionally include sources across the political spectrum
              to ensure multiple perspectives.
            </p>
          </div>

          <div className="criteria-item">
            <h4>Professional Standards</h4>
            <p>
              Adherence to journalism ethics codes and professional standards
              organizations.
            </p>
          </div>

          <div className="criteria-item">
            <h4>Technical Accessibility</h4>
            <p>
              Must provide RSS feeds or public APIs that don't require
              authentication or payment.
            </p>
          </div>
        </div>

        <p className="note">
          <strong>Important:</strong> Inclusion does not imply endorsement.
          We include sources we disagree with to ensure perspective diversity.
        </p>
      </section>

      <section className="transparency-section card">
        <h2>Bias Detection Methodology</h2>
        
        <h3>What We Check For</h3>
        <ul>
          <li>
            <strong>Loaded Language:</strong> Emotionally charged words and phrases
            that reveal bias (e.g., "radical," "extreme," "heroic")
          </li>
          <li>
            <strong>Unsupported Claims:</strong> Statements presented as fact
            without clear source attribution
          </li>
          <li>
            <strong>Attribution Quality:</strong> Whether sources are named,
            credible, and relevant
          </li>
          <li>
            <strong>Framing:</strong> How issues are presented and what context
            is included or excluded
          </li>
          <li>
            <strong>Perspective Balance:</strong> Distribution of viewpoints
            in source articles
          </li>
        </ul>

        <h3>Limitations</h3>
        <p>Our bias detection is:</p>
        <ul>
          <li>Automated and may miss subtle biases</li>
          <li>Based on heuristics that aren't universally agreed upon</li>
          <li>Unable to detect all forms of bias (e.g., selection bias)</li>
          <li>Continuously evolving as we improve our methods</li>
        </ul>
      </section>

      <section className="transparency-section card">
        <h2>Privacy & Data Collection</h2>
        
        <div className="privacy-statement">
          <h3>What We DON'T Collect:</h3>
          <ul>
            <li>No cookies (except essential session cookies)</li>
            <li>No user tracking or analytics</li>
            <li>No IP address logging</li>
            <li>No user accounts or profiles</li>
            <li>No personalization based on your behavior</li>
            <li>No data sharing with third parties</li>
          </ul>

          <h3>What We DO Collect:</h3>
          <ul>
            <li>
              Server access logs (temporary, for security and debugging only)
            </li>
            <li>
              Error reports (no personal information, automatically deleted)
            </li>
          </ul>
        </div>
      </section>

      <section className="transparency-section card">
        <h2>Funding & Independence</h2>
        
        <p>
          Talk-Less is an open-source project with no commercial funding or
          advertising. The project is maintained by volunteers committed to
          transparent news aggregation.
        </p>
        
        <p>
          We accept no funding from:
        </p>
        <ul>
          <li>Political organizations or campaigns</li>
          <li>News organizations we aggregate from</li>
          <li>Advertisers or marketing companies</li>
          <li>Any entity that would create conflicts of interest</li>
        </ul>
      </section>

      <section className="transparency-section card">
        <h2>Algorithm Transparency</h2>
        
        <p>
          All our code is open source under the AGPL-3.0 license. You can review:
        </p>
        
        <ul>
          <li>
            <strong>Clustering parameters:</strong> How articles are grouped together
          </li>
          <li>
            <strong>Summary prompts:</strong> Exact prompts sent to language models
          </li>
          <li>
            <strong>Bias detection rules:</strong> All patterns and thresholds
          </li>
          <li>
            <strong>Source selection logic:</strong> How sources are chosen and weighted
          </li>
        </ul>

        <p>
          <a
            href="https://github.com/yourusername/Talk-Less"
            target="_blank"
            rel="noopener noreferrer"
            className="button"
          >
            View Source Code on GitHub →
          </a>
        </p>
      </section>

      <section className="transparency-section card">
        <h2>Known Limitations</h2>
        
        <div className="limitations-list">
          <div className="limitation-item">
            <h4>Language Model Errors</h4>
            <p>
              AI-generated summaries can misrepresent source content, miss important
              context, or reflect biases in training data.
            </p>
          </div>

          <div className="limitation-item">
            <h4>Source Selection Bias</h4>
            <p>
              Our choice of which sources to include involves subjective judgments
              about credibility and relevance.
            </p>
          </div>

          <div className="limitation-item">
            <h4>English Language Focus</h4>
            <p>
              Currently, we primarily aggregate English-language sources, missing
              important international perspectives.
            </p>
          </div>

          <div className="limitation-item">
            <h4>Coverage Gaps</h4>
            <p>
              We can't cover all topics or sources. Some stories may be underrepresented
              or missing entirely.
            </p>
          </div>

          <div className="limitation-item">
            <h4>Bias Detection Imperfection</h4>
            <p>
              Our automated bias detection has false positives and misses subtle
              forms of bias.
            </p>
          </div>

          <div className="limitation-item">
            <h4>Real-Time Limitations</h4>
            <p>
              There's a delay between article publication and summary generation.
              We're not suitable for breaking news.
            </p>
          </div>
        </div>
      </section>

      <section className="transparency-section card">
        <h2>Accountability & Feedback</h2>
        
        <p>
          We welcome scrutiny and feedback. If you find errors, biases, or problems:
        </p>
        
        <ul>
          <li>
            Open an issue on{' '}
            <a
              href="https://github.com/yourusername/Talk-Less/issues"
              target="_blank"
              rel="noopener noreferrer"
            >
              GitHub
            </a>
          </li>
          <li>Review and suggest changes to our source list</li>
          <li>Propose improvements to bias detection rules</li>
          <li>Contribute code to fix issues you identify</li>
        </ul>
      </section>

      <section className="transparency-section card cta-section">
        <h2>Questions?</h2>
        <p>
          For more information about our approach and principles:
        </p>
        <div className="cta-buttons">
          <Link to="/about" className="button">
            Learn About Our Mission
          </Link>
          <Link to="/sources" className="button">
            View Our Sources
          </Link>
        </div>
      </section>
    </div>
  );
}

export default Transparency;
