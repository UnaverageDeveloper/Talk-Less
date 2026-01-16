/*
 * Talk-Less Source List Component
 * Copyright (C) 2024 Talk-Less Contributors
 * Licensed under AGPL-3.0-or-later
 */

import React, { useState, useEffect } from 'react';
import './SourceList.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function SourceList() {
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchSources();
  }, []);

  const fetchSources = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/sources`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setSources(data.sources || data);
    } catch (err) {
      console.error('Error fetching sources:', err);
      setError('Failed to load sources. Please check if the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading sources</div>;
  }

  if (error) {
    return (
      <div className="error">
        <div className="error-title">Error</div>
        <p>{error}</p>
        <button onClick={fetchSources}>Retry</button>
      </div>
    );
  }

  if (sources.length === 0) {
    return (
      <div className="empty-state">
        <h2>No Sources Available</h2>
        <p>News sources have not been configured yet.</p>
      </div>
    );
  }

  return (
    <div className="source-list">
      <div className="page-header">
        <h1>News Sources</h1>
        <p className="page-description">
          We aggregate news from diverse sources representing multiple perspectives.
          Our selection criteria prioritize editorial independence, fact-checking standards,
          and ideological diversity.
        </p>
      </div>

      <section className="sources-info">
        <h2>Source Selection Principles</h2>
        <ul>
          <li><strong>Diversity:</strong> Sources span the ideological spectrum</li>
          <li><strong>Credibility:</strong> Established editorial standards and fact-checking</li>
          <li><strong>Transparency:</strong> Clear attribution and sourcing practices</li>
          <li><strong>Independence:</strong> Editorial independence from external influence</li>
        </ul>
      </section>

      <div className="sources-grid">
        {sources.map((source, idx) => (
          <article key={idx} className="source-card card">
            <div className="source-card-header">
              <h3 className="source-card-title">{source.name}</h3>
              {source.bias_label && (
                <span className="badge badge-secondary">{source.bias_label}</span>
              )}
            </div>

            {source.url && (
              <a
                href={source.url}
                target="_blank"
                rel="noopener noreferrer"
                className="source-url"
              >
                {source.url}
              </a>
            )}

            {source.description && (
              <p className="source-description">{source.description}</p>
            )}

            <div className="source-metadata">
              {source.country && (
                <div className="source-meta-item">
                  <strong>Country:</strong> {source.country}
                </div>
              )}
              {source.language && (
                <div className="source-meta-item">
                  <strong>Language:</strong> {source.language}
                </div>
              )}
              {source.type && (
                <div className="source-meta-item">
                  <strong>Type:</strong> {source.type}
                </div>
              )}
            </div>

            {source.fetch_method && (
              <div className="source-tech">
                <small>Method: {source.fetch_method}</small>
              </div>
            )}
          </article>
        ))}
      </div>

      <section className="sources-methodology">
        <h2>Methodology</h2>
        <p>
          Sources are selected through a rigorous evaluation process considering:
        </p>
        <ol>
          <li>Historical accuracy and correction policies</li>
          <li>Editorial independence and transparency</li>
          <li>Fact-checking practices and source attribution</li>
          <li>Representation of diverse perspectives</li>
          <li>Professional journalism standards</li>
        </ol>
        <p>
          We continuously monitor source quality and adjust our selection as needed.
          For detailed methodology, see our <a href="/transparency">Transparency page</a>.
        </p>
      </section>
    </div>
  );
}

export default SourceList;
