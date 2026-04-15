import React from 'react';

const RADIUS = 60;
const CIRCUMFERENCE = 2 * Math.PI * RADIUS;

const ConfidenceRing = ({ value }) => {
  const dash = (value / 100) * CIRCUMFERENCE;
  return (
    <div className="confidence-ring-container">
      <svg className="confidence-ring-svg" viewBox="0 0 140 140">
        <defs>
          <linearGradient id="ringGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%"   stopColor="#8b5cf6" />
            <stop offset="50%"  stopColor="#6366f1" />
            <stop offset="100%" stopColor="#06b6d4" />
          </linearGradient>
        </defs>
        <circle className="confidence-ring-track" cx="70" cy="70" r={RADIUS} />
        <circle
          className="confidence-ring-fill"
          cx="70" cy="70" r={RADIUS}
          strokeDasharray={`${dash} ${CIRCUMFERENCE - dash}`}
          strokeDashoffset={0}
        />
      </svg>
      <div className="confidence-ring-label">
        <span className="confidence-value">{value}%</span>
        <span className="confidence-label">Match</span>
      </div>
    </div>
  );
};

const VerifyResult = ({ result, loading }) => {
  if (loading) {
    return (
      <div className="result-panel">
        <div className="spinner" />
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Analyzing fingerprint…</p>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="result-panel result-panel--empty">
        <div style={{ fontSize: '4rem', opacity: 0.4 }}>🔍</div>
        <h3 style={{ color: 'var(--text-muted)' }}>Awaiting Analysis</h3>
        <p style={{ textAlign: 'center', fontSize: '0.85rem', maxWidth: 220 }}>
          Upload a file on the left to extract its ownership signature.
        </p>
      </div>
    );
  }

  if (!result.found) {
    return (
      <div className="result-panel">
        <div style={{ fontSize: '3.5rem' }}>❓</div>
        <h3 style={{ color: 'var(--accent-warn)' }}>No Fingerprint Found</h3>
        <p style={{ textAlign: 'center', fontSize: '0.85rem', maxWidth: 260 }}>
          This file does not appear to contain a DataDNA watermark,
          or the watermark has been removed/damaged.
        </p>
        <div className="badge badge-amber">Unverified</div>
      </div>
    );
  }

  return (
    <div className="result-panel animate-fadeInUp">
      <div className="badge badge-green" style={{ marginBottom: 'var(--space-sm)' }}>
        ✅ Owner Identified
      </div>

      <ConfidenceRing value={result.confidence} />

      <div className="owner-result-card" style={{ marginTop: 'var(--space-sm)' }}>
        <span className="owner-result-label">👤 Original Owner</span>
        <span className="owner-result-value">{result.owner}</span>
      </div>

      {result.watermark_id && (
        <div className="owner-result-card">
          <span className="owner-result-label">🔑 Watermark ID</span>
          <span className="owner-result-value" style={{ fontSize: '0.85rem' }}>{result.watermark_id}</span>
        </div>
      )}

      {result.embed_date && (
        <div className="owner-result-card">
          <span className="owner-result-label">📅 Embedded On</span>
          <span className="owner-result-value" style={{ fontSize: '0.85rem' }}>
            {new Date(result.embed_date).toLocaleDateString('en-IN', { dateStyle: 'long' })}
          </span>
        </div>
      )}
    </div>
  );
};

export default VerifyResult;
