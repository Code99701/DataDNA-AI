import React from 'react';

const UploadResult = ({ file }) => {
  if (!file) return null;
  
  return (
    <div style={{ marginTop: '2rem' }} className="result-card">
      <h3 style={{ color: 'var(--accent)' }}>Ready to process</h3>
      <p style={{ marginTop: '0.5rem', color: 'var(--text-muted)' }}>
        Your file '{file.name}' is queued. Click generate to construct ownership embedding.
      </p>
    </div>
  );
};

export default UploadResult;
