/*
 * Talk-Less Summary Detail Component
 * Copyright (C) 2024 Talk-Less Contributors
 * Licensed under AGPL-3.0-or-later
 */

import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import BiasIndicators from './BiasIndicators';
import './SummaryDetail.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function SummaryDetail() {
  const { id } = useParams();
  const [summary, setSummary] = useState(null);
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchSummaryDetail();
  }, [id]);

  const fetchSummaryDetail = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/summaries/${id}`);
      
      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('Summary not found');
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setSummary(data);

      if (data.source_articles && data.source_articles.length > 0) {
        setSources(data.source_articles);
      }
    } catch (err) {
      console.error('Error fetching summary:', err);
      setError(err.message || 'Failed to load summary');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Unknown date';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const extractCitations = (text) => {
    if (!text) return [];
    const citationRegex = /\[(\d+)\]/g;
    const matches = [...text.matchAll(citationRegex)];
    return matches.map(m => parseInt(m[1]));
  };

  if (loading) {
    return <div className="loading">Loading summary details</div>;
  }

  if (error) {
    return (
      <div className="error">
        <div className="error-title">Error</div>
        <p>{error}</p>
        <Link to="/" className="button">Back to Home</Link>
      </div>
    );
  }

  if (!summary) {
    return (
      <div className="empty-state">
        <h2>Summary Not Found</h2>
        <p>The requested summary could not be found.</p>
        <Link to="/" className="button">Back to Home</Link>
      </div>
    );
  }

  const citations = extractCitations(summary.summary_text);

  return (
    <div className="summary-detail">
      <nav className="breadcrumb" aria-label="Breadcrumb">
        <Link to="/">Home</Link>
        <span className="breadcrumb-separator">/</span>
        <span>Summary</span>
      </nav>

      <article className="detail-card card">
        <header className="detail-header">
          <h1>{summary.title || 'Untitled Summary'}</h1>
          <div className="detail-meta">
            <time dateTime={summary.created_at}>
              {formatDate(summary.created_at)}
            </time>
            {sources.length > 0 && (
              <span className="sources-count">
                {' • '}{sources.length} source{sources.length !== 1 ? 's' : ''}
              </span>
            )}
          </div>
        </header>

        <section className="detail-content">
          <h2 className="section-title">Summary</h2>
          <div className="summary-text-full">
            {summary.summary_text?.split('\n').map((paragraph, idx) => (
              <p key={idx}>{paragraph}</p>
            ))}
          </div>
        </section>

        {summary.bias_indicators && (
          <section className="detail-bias">
            <h2 className="section-title">Transparency Metrics</h2>
            <BiasIndicators indicators={summary.bias_indicators} compact={false} />
          </section>
        )}

        {sources.length > 0 && (
          <section className="detail-sources">
            <h2 className="section-title">Source Articles</h2>
            <div className="sources-list">
              {sources.map((source, idx) => (
                <article key={idx} className="source-item card">
                  <div className="source-header">
                    <h3 className="source-title">
                      [{idx + 1}] {source.title || 'Untitled'}
                    </h3>
                    {source.source_name && (
                      <div className="source-name badge badge-secondary">
                        {source.source_name}
                      </div>
                    )}
                  </div>
                  
                  {source.url && (
                    <a
                      href={source.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="source-link"
                    >
                      View Original Article →
                    </a>
                  )}
                  
                  {source.published_date && (
                    <div className="source-meta">
                      Published: {formatDate(source.published_date)}
                    </div>
                  )}

                  {source.perspective && (
                    <div className="source-perspective">
                      <strong>Perspective:</strong> {source.perspective}
                    </div>
                  )}
                </article>
              ))}
            </div>
          </section>
        )}

        <section className="detail-disclaimer">
          <h3>Disclaimer</h3>
          <p>
            This summary is generated from multiple news sources and may not capture all nuances.
            Always consult the original source articles for complete context and verification.
          </p>
        </section>
      </article>

      <div className="detail-actions">
        <Link to="/" className="button">← Back to Summaries</Link>
      </div>
    </div>
  );
}

export default SummaryDetail;
