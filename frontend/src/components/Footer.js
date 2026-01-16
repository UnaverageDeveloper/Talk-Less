/*
 * Talk-Less Footer Component
 * Copyright (C) 2024 Talk-Less Contributors
 * Licensed under AGPL-3.0-or-later
 */

import React from 'react';
import { Link } from 'react-router-dom';
import './Footer.css';

function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer no-print">
      <div className="footer-container">
        <div className="footer-section">
          <h3>Talk-Less</h3>
          <p>
            Transparent, multi-perspective news aggregation without tracking or manipulation.
          </p>
        </div>

        <div className="footer-section">
          <h4>Navigation</h4>
          <ul className="footer-links">
            <li><Link to="/">Home</Link></li>
            <li><Link to="/sources">Sources</Link></li>
            <li><Link to="/transparency">Transparency</Link></li>
            <li><Link to="/about">About</Link></li>
          </ul>
        </div>

        <div className="footer-section">
          <h4>Principles</h4>
          <ul className="footer-links">
            <li>No User Tracking</li>
            <li>Open Source (AGPL-3.0)</li>
            <li>Multi-Perspective Coverage</li>
            <li>Full Transparency</li>
          </ul>
        </div>

        <div className="footer-section">
          <h4>Resources</h4>
          <ul className="footer-links">
            <li>
              <a
                href="https://github.com/yourusername/Talk-Less"
                target="_blank"
                rel="noopener noreferrer"
              >
                GitHub Repository
              </a>
            </li>
            <li>
              <a
                href="https://www.gnu.org/licenses/agpl-3.0.html"
                target="_blank"
                rel="noopener noreferrer"
              >
                AGPL-3.0 License
              </a>
            </li>
          </ul>
        </div>
      </div>

      <div className="footer-bottom">
        <p>
          © {currentYear} Talk-Less Contributors. Licensed under{' '}
          <a
            href="https://www.gnu.org/licenses/agpl-3.0.html"
            target="_blank"
            rel="noopener noreferrer"
          >
            AGPL-3.0-or-later
          </a>
        </p>
        <p className="footer-disclaimer">
          This service provides summaries of news articles. We make no claims about accuracy
          or completeness. Always verify information from original sources.
        </p>
      </div>
    </footer>
  );
}

export default Footer;
