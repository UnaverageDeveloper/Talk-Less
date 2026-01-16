/*
 * Talk-Less Summary List Component
 * Copyright (C) 2024 Talk-Less Contributors
 * Licensed under AGPL-3.0-or-later
 */

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import BiasIndicators from './BiasIndicators';
import './SummaryList.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function SummaryList() {
  const [summaries, setSummaries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [hasMore, setHasMore] = useState(true);

  const itemsPerPage = 10;

  useEffect(() => {
    fetchSummaries();
  }, [page]);

  const fetchSummaries = async () => {
    setLoading(true);
    setError(null);

    try {
      const skip = (page - 1) * itemsPerPage;
      const response = await fetch(
        `${API_BASE_URL}/api/summaries?skip=${skip}&limit=${itemsPerPage}`
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setSummaries(data.summaries || data);
      
      if (data.total !== undefined) {
        const total = Math.ceil(data.total / itemsPerPage);
        setTotalPages(total);
        setHasMore(page < total);
      } else {
        setHasMore(data.length === itemsPerPage);
      }
    } catch (err) {
      console.error('Error fetching summaries:', err);
      setError('Failed to load summaries. Please check if the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const handlePrevPage = () => {
    if (page > 1) {
      setPage(page - 1);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const handleNextPage = () => {
    if (hasMore) {
      setPage(page + 1);
      window.scrollTo({ top: 0, behavior: 'smooth' });
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

  if (loading && summaries.length === 0) {
    return <div className="loading">Loading summaries</div>;
  }

  if (error) {
    return (
      <div className="error">
        <div className="error-title">Error</div>
        <p>{error}</p>
        <button onClick={fetchSummaries}>Retry</button>
      </div>
    );
  }

  if (!loading && summaries.length === 0) {
    return (
      <div className="empty-state">
        <h2>No Summaries Available</h2>
        <p>Check back later for news summaries.</p>
      </div>
    );
  }

  return (
    <div className="summary-list">
      <div className="page-header">
        <h1>Latest News Summaries</h1>
        <p className="page-description">
          Multi-perspective news summaries aggregated from diverse sources.
          All summaries include source attribution and transparency metrics.
        </p>
      </div>

      <div className="summaries-container">
        {summaries.map((summary) => (
          <article key={summary.id} className="summary-card card">
            <div className="summary-header">
              <Link to={`/summary/${summary.id}`} className="summary-title-link">
                <h2 className="card-title">{summary.title || 'Untitled Summary'}</h2>
              </Link>
              <div className="card-meta">
                <time dateTime={summary.created_at}>
                  {formatDate(summary.created_at)}
                </time>
                {summary.sources_count && (
                  <span className="sources-count">
                    {' • '}{summary.sources_count} source{summary.sources_count !== 1 ? 's' : ''}
                  </span>
                )}
              </div>
            </div>

            <div className="summary-content">
              <p className="summary-text">
                {summary.summary_text?.substring(0, 300)}
                {summary.summary_text?.length > 300 ? '...' : ''}
              </p>
            </div>

            {summary.bias_indicators && (
              <BiasIndicators indicators={summary.bias_indicators} compact={true} />
            )}

            <div className="summary-footer">
              <Link to={`/summary/${summary.id}`} className="read-more-link">
                Read Full Summary →
              </Link>
            </div>
          </article>
        ))}
      </div>

      {(page > 1 || hasMore) && (
        <div className="pagination">
          <button
            onClick={handlePrevPage}
            disabled={page === 1}
            aria-label="Previous page"
          >
            ← Previous
          </button>
          
          <span className="page-info">
            Page {page} {totalPages > 1 && `of ${totalPages}`}
          </span>
          
          <button
            onClick={handleNextPage}
            disabled={!hasMore}
            aria-label="Next page"
          >
            Next →
          </button>
        </div>
      )}

      {loading && (
        <div className="loading-overlay">
          <div className="loading">Loading</div>
        </div>
      )}
    </div>
  );
}

export default SummaryList;
