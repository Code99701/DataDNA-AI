import React from 'react';

const VerifyResult = ({ data, isProcessing }) => {
  if (isProcessing) {
    return (
      <div className="result-card">
        <h2 style={{ color: 'var(--text-muted)' }}>AI Processing...</h2>
        <p style={{ marginTop: '1rem', color: 'var(--accent)' }}>Running Deep Autoencoder...</p>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="result-card">
        <div style={{ opacity: 0.3 }}>
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="16" x2="12" y2="12"></line>
            <line x1="12" y1="8" x2="12.01" y2="8"></line>
          </svg>
        </div>
        <h3 style={{ marginTop: '1rem', color: 'var(--text-muted)' }}>Awaiting Analysis</h3>
        <p style={{ marginTop: '0.5rem', color: 'rgba(255,255,255,0.4)', fontSize: '0.9rem' }}>
          Upload a file on the left to extract its ownership signature.
        </p>
      </div>
    );
  }

  return (
    <div className="result-card animation-fadeIn">
      <h2 style={{ marginBottom: '2rem' }}>Extraction Result</h2>
      
      <div className="confidence-ring" style={{ '--percentage': data.confidence }}>
        <span className="confidence-value">{data.confidence}%</span>
      </div>
      <p style={{ color: 'var(--text-muted)', marginBottom: '2rem', fontSize: '0.9rem' }}>Match Confidence Level</p>
      
      <div className="owner-info">
        <span className="owner-label">Original Owner</span>
        <span className="owner-name">{data.owner}</span>
      </div>
    </div>
  );
};

export default VerifyResult;
