import React from 'react';
import './ResultsDisplay.css';

function ResultsDisplay({ results }) {
  const protocols = ['BB84', 'B92', 'E91', 'BBM92'];

  const formatNumber = (value, decimals = 2) => {
    if (value === null || value === undefined) return '-';
    return typeof value === 'number' ? value.toFixed(decimals) : value;
  };

  const formatKeyRate = (value) => {
    if (value === null || value === undefined) return '-';
    return value.toLocaleString('en-US', { maximumFractionDigits: 0 });
  };

  return (
    <div className="results-container">
      <h2>Simulation Results</h2>
      <p className="results-subtitle">Comparison of all 4 QKD protocols</p>
      
      <div className="results-grid">
        {protocols.map(protocol => {
          const result = results[protocol];
          if (!result) return null;

          return (
            <div key={protocol} className="protocol-card">
              <div className="protocol-header">
                <h3>{protocol}</h3>
                <div className="protocol-badge">{getProtocolDescription(protocol)}</div>
              </div>

              <div className="results-list">
                <div className="result-item">
                  <span className="result-label">Key Length</span>
                  <span className="result-value">
                    {result.key_length ? result.key_length.toLocaleString() : '-'}
                  </span>
                </div>

                <div className="result-item">
                  <span className="result-label">Key Rate</span>
                  <span className="result-value">
                    {formatKeyRate(result.key_rate)} Hz
                  </span>
                </div>

                <div className="result-item">
                  <span className="result-label">QBER</span>
                  <span className="result-value qber">
                    {formatNumber(result.qber)} %
                  </span>
                </div>

                {result.s_statistic !== null && result.s_statistic !== undefined && (
                  <div className="result-item">
                    <span className="result-label">S Statistic</span>
                    <span className="result-value s-stat">
                      {formatNumber(result.s_statistic)}
                    </span>
                  </div>
                )}

                <div className="result-item">
                  <span className="result-label">Combined Efficiency</span>
                  <span className="result-value">
                    {formatNumber(result.combined_efficiency)} %
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="results-footer">
        <h3>Protocol Comparison Notes</h3>
        <div className="comparison-notes">
          <div className="note">
            <strong>BB84:</strong> Single-qubit protocol using rectilinear and diagonal bases. ~50% key retention after basis reconciliation.
          </div>
          <div className="note">
            <strong>B92:</strong> Simplified BB84 using non-orthogonal states. Lower key rate (~25%) but simpler implementation.
          </div>
          <div className="note">
            <strong>E91:</strong> Entanglement-based with Bell test (S statistic). Security verified through CHSH inequality. ~33% key retention.
          </div>
          <div className="note">
            <strong>BBM92:</strong> Simplified entanglement-based protocol. Similar to BB84 but uses entangled pairs. ~50% key retention.
          </div>
        </div>
      </div>
    </div>
  );
}

function getProtocolDescription(protocol) {
  const descriptions = {
    'BB84': 'Single-qubit',
    'B92': 'Non-orthogonal',
    'E91': 'Bell-based',
    'BBM92': 'Entanglement'
  };
  return descriptions[protocol] || '';
}

export default ResultsDisplay;
