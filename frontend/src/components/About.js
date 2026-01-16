/*
 * Talk-Less About Page Component
 * Copyright (C) 2024 Talk-Less Contributors
 * Licensed under AGPL-3.0-or-later
 */

import React from 'react';
import { Link } from 'react-router-dom';
import './About.css';

function About() {
  return (
    <div className="about-page">
      <div className="page-header">
        <h1>About Talk-Less</h1>
        <p className="page-subtitle">
          Transparent, Multi-Perspective News Aggregation
        </p>
      </div>

      <section className="about-section card">
        <h2>Our Mission</h2>
        <p>
          Talk-Less exists to provide news summaries that respect your intelligence and autonomy.
          We believe you deserve transparent, multi-perspective news coverage without manipulation,
          tracking, or hidden agendas.
        </p>
        <p>
          In an age of information overload and algorithmic news feeds, we offer an alternative:
          straightforward aggregation of diverse perspectives with complete transparency about
          our methods and limitations.
        </p>
      </section>

      <section className="about-section card">
        <h2>Core Principles</h2>
        
        <div className="principles-grid">
          <div className="principle-item">
            <h3>🔒 No Tracking</h3>
            <p>
              We don't track you. No cookies, no analytics, no user profiles.
              Your privacy is absolute.
            </p>
          </div>

          <div className="principle-item">
            <h3>🌐 Multi-Perspective</h3>
            <p>
              We aggregate from diverse sources across the ideological spectrum.
              You see multiple viewpoints, not just one narrative.
            </p>
          </div>

          <div className="principle-item">
            <h3>🔍 Full Transparency</h3>
            <p>
              Our methods, sources, and algorithms are open. We show you
              exactly how summaries are created.
            </p>
          </div>

          <div className="principle-item">
            <h3>⚖️ No Editorial Agenda</h3>
            <p>
              We don't push a political viewpoint. Our goal is to present
              diverse perspectives fairly.
            </p>
          </div>

          <div className="principle-item">
            <h3>📖 Open Source</h3>
            <p>
              All our code is open source (AGPL-3.0). You can verify,
              audit, and contribute.
            </p>
          </div>

          <div className="principle-item">
            <h3>🎯 Transformative Summaries</h3>
            <p>
              Our summaries add value by synthesizing multiple perspectives,
              not just copying content.
            </p>
          </div>
        </div>
      </section>

      <section className="about-section card">
        <h2>How It Works</h2>
        
        <div className="process-steps">
          <div className="process-step">
            <div className="step-number">1</div>
            <div className="step-content">
              <h3>Article Collection</h3>
              <p>
                We collect articles from diverse news sources using RSS feeds
                and public APIs. No paywalled or login-required content.
              </p>
            </div>
          </div>

          <div className="process-step">
            <div className="step-number">2</div>
            <div className="step-content">
              <h3>Clustering & Analysis</h3>
              <p>
                Articles about the same topic are grouped together using
                semantic similarity. We identify different perspectives
                within each cluster.
              </p>
            </div>
          </div>

          <div className="process-step">
            <div className="step-number">3</div>
            <div className="step-content">
              <h3>Summary Generation</h3>
              <p>
                An AI model creates a transformative summary that synthesizes
                multiple perspectives with clear citations to source articles.
              </p>
            </div>
          </div>

          <div className="process-step">
            <div className="step-number">4</div>
            <div className="step-content">
              <h3>Bias Detection</h3>
              <p>
                Automated checks identify loaded language, unsupported claims,
                and perspective imbalances. Results are shown transparently.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="about-section card">
        <h2>What We're Not</h2>
        <ul className="not-list">
          <li>
            <strong>Not a news organization:</strong> We don't create original
            reporting. We aggregate and summarize existing journalism.
          </li>
          <li>
            <strong>Not perfect:</strong> Automated systems make mistakes. We're
            transparent about limitations and continuously improving.
          </li>
          <li>
            <strong>Not comprehensive:</strong> We can't cover everything. Source
            selection involves tradeoffs we document openly.
          </li>
          <li>
            <strong>Not a filter bubble:</strong> Unlike personalized news feeds,
            everyone sees the same summaries based on source diversity, not
            your preferences.
          </li>
        </ul>
      </section>

      <section className="about-section card">
        <h2>Limitations & Disclaimers</h2>
        <p>
          We believe in radical transparency about what we can and cannot do:
        </p>
        <ul>
          <li>AI summaries may miss nuance or make errors</li>
          <li>Bias detection is imperfect and evolving</li>
          <li>Source selection is never fully "neutral"</li>
          <li>We depend on the quality of source articles</li>
          <li>No aggregator can replace reading original sources</li>
        </ul>
        <p>
          Always verify important information from original sources.
        </p>
      </section>

      <section className="about-section card">
        <h2>Get Involved</h2>
        <p>
          Talk-Less is open source and community-driven. Ways to participate:
        </p>
        <ul>
          <li>
            <strong>Review our code:</strong> Check our{' '}
            <a
              href="https://github.com/yourusername/Talk-Less"
              target="_blank"
              rel="noopener noreferrer"
            >
              GitHub repository
            </a>
          </li>
          <li>
            <strong>Report issues:</strong> Found a bug or bias? Open an issue
          </li>
          <li>
            <strong>Suggest sources:</strong> Propose news sources we should add
          </li>
          <li>
            <strong>Contribute code:</strong> Help improve our algorithms
          </li>
        </ul>
      </section>

      <section className="about-section card cta-section">
        <h2>Learn More</h2>
        <div className="cta-buttons">
          <Link to="/transparency" className="button">
            View Transparency Report
          </Link>
          <Link to="/sources" className="button">
            Browse Our Sources
          </Link>
        </div>
      </section>
    </div>
  );
}

export default About;
