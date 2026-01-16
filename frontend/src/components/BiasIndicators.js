/*
 * Talk-Less Bias Indicators Component
 * Copyright (C) 2024 Talk-Less Contributors
 * Licensed under AGPL-3.0-or-later
 */

import React from 'react';
import './BiasIndicators.css';

function BiasIndicators({ indicators, compact = false }) {
  if (!indicators) {
    return null;
  }

  const {
    loaded_language_count = 0,
    unsupported_claims_count = 0,
    perspective_balance = {},
    source_diversity_score = 0,
    flags = []
  } = indicators;

  const getScoreClass = (score) => {
    if (score >= 0.7) return 'score-good';
    if (score >= 0.4) return 'score-medium';
    return 'score-low';
  };

  const getCountClass = (count, threshold = 3) => {
    if (count === 0) return 'count-good';
    if (count < threshold) return 'count-medium';
    return 'count-high';
  };

  if (compact) {
    return (
      <div className="bias-indicators compact">
        <div className="indicator-compact">
          <span className="indicator-label">Source Diversity:</span>
          <span className={`indicator-value ${getScoreClass(source_diversity_score)}`}>
            {(source_diversity_score * 100).toFixed(0)}%
          </span>
        </div>
        
        {loaded_language_count > 0 && (
          <div className="indicator-compact">
            <span className="indicator-label">Loaded Language:</span>
            <span className={`indicator-value ${getCountClass(loaded_language_count)}`}>
              {loaded_language_count}
            </span>
          </div>
        )}
        
        {flags && flags.length > 0 && (
          <div className="indicator-flags-compact">
            {flags.slice(0, 2).map((flag, idx) => (
              <span key={idx} className="badge badge-warning" title={flag}>
                ⚠
              </span>
            ))}
            {flags.length > 2 && (
              <span className="badge badge-secondary">+{flags.length - 2}</span>
            )}
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="bias-indicators full">
      <div className="indicators-grid">
        <div className="indicator-card">
          <h4 className="indicator-title">Source Diversity</h4>
          <div className={`indicator-score ${getScoreClass(source_diversity_score)}`}>
            {(source_diversity_score * 100).toFixed(0)}%
          </div>
          <p className="indicator-description">
            Measures the diversity of perspectives across source articles
          </p>
        </div>

        <div className="indicator-card">
          <h4 className="indicator-title">Loaded Language</h4>
          <div className={`indicator-count ${getCountClass(loaded_language_count)}`}>
            {loaded_language_count}
          </div>
          <p className="indicator-description">
            Number of emotionally charged or biased phrases detected
          </p>
        </div>

        <div className="indicator-card">
          <h4 className="indicator-title">Unsupported Claims</h4>
          <div className={`indicator-count ${getCountClass(unsupported_claims_count)}`}>
            {unsupported_claims_count}
          </div>
          <p className="indicator-description">
            Statements lacking clear source attribution
          </p>
        </div>
      </div>

      {perspective_balance && Object.keys(perspective_balance).length > 0 && (
        <div className="perspective-section">
          <h4>Perspective Balance</h4>
          <div className="perspective-chart">
            {Object.entries(perspective_balance).map(([perspective, count]) => (
              <div key={perspective} className="perspective-item">
                <span className="perspective-label">{perspective}:</span>
                <div className="perspective-bar-container">
                  <div
                    className="perspective-bar"
                    style={{
                      width: `${Math.min(100, (count / 10) * 100)}%`
                    }}
                  />
                  <span className="perspective-count">{count}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {flags && flags.length > 0 && (
        <div className="flags-section">
          <h4>Transparency Flags</h4>
          <ul className="flags-list">
            {flags.map((flag, idx) => (
              <li key={idx} className="flag-item">
                <span className="flag-icon">⚠</span>
                {flag}
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="indicators-note">
        <p>
          <strong>Note:</strong> These metrics are automatically generated and may not be perfect.
          They serve as transparency indicators, not definitive judgments.
        </p>
      </div>
    </div>
  );
}

export default BiasIndicators;
