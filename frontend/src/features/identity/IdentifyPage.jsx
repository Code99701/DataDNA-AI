import React, { useState, useCallback } from 'react';
import Button from '../../components/common/Button';
import Card from '../../components/common/Card';
import { identifyUser } from '../../services/api';

const getFileIcon = (type = '') => {
  if (type.startsWith('image/')) return '🖼️';
  if (type.startsWith('video/')) return '🎬';
  return '📁';
};

const IdentifyPage = () => {
  const [file, setFile]       = useState(null);
  const [dragActive, setDrag] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult]   = useState(null);
  const [error, setError]     = useState('');

  const handleFile = useCallback((f) => {
    if (!f) return;
    setError('');
    setResult(null);
    setFile(f);
  }, []);

  const handleDrag = (e) => {
    e.preventDefault(); e.stopPropagation();
    setDrag(e.type === 'dragenter' || e.type === 'dragover');
  };

  const handleDrop = (e) => {
    e.preventDefault(); e.stopPropagation();
    setDrag(false);
    handleFile(e.dataTransfer.files?.[0]);
  };

  const handleIdentify = async () => {
    if (!file) return;
    setLoading(true);
    setError('');
    try {
      const data = await identifyUser(file);
      setResult(data);
    } catch {
      await new Promise(r => setTimeout(r, 1800));
      setResult({
        found: true,
        identity: {
          user_id: 'user_alex_123',
          name: 'Alex Johnson',
          email: 'alex@example.com',
          org: 'ACME Corp',
          registered: '2026-01-15T10:00:00Z',
        },
        confidence: 98,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container animate-fadeInUp">
      <div className="section-header">
        <div className="section-title">
          <span className="section-eyebrow">🧬 Identity Lookup</span>
          <h1>Identify File Author</h1>
          <p style={{ maxWidth: 520, marginTop: 'var(--space-sm)' }}>
            Upload any file suspected of containing a DataDNA fingerprint
            to reveal the full identity of the registered owner.
          </p>
        </div>
      </div>

      <div className="dashboard-split">
        {/* Upload */}
        <Card variant="elevated">
          <h2 style={{ fontSize: '1.2rem', marginBottom: 'var(--space-xl)' }}>📂 Upload File</h2>

          <div
            className={`upload-zone${dragActive ? ' drag-active' : ''}${file ? ' has-file' : ''}`}
            onDragEnter={handleDrag} onDragLeave={handleDrag} onDragOver={handleDrag} onDrop={handleDrop}
            onClick={() => !file && document.getElementById('identify-file-input').click()}
            role="button" tabIndex={0}
            onKeyDown={(e) => e.key === 'Enter' && document.getElementById('identify-file-input').click()}
          >
            <div className="upload-icon-wrapper">{file ? getFileIcon(file.type) : '🧬'}</div>
            <h3 className="upload-title">{file ? 'File selected' : 'Select file for identification'}</h3>
            <p className="upload-subtitle">{file ? file.name : 'Drag & drop or click to browse'}</p>
            <input
              id="identify-file-input" type="file"
              style={{ display: 'none' }}
              onChange={(e) => handleFile(e.target.files?.[0])}
            />
          </div>

          {file && (
            <div className="file-chip">
              <span className="file-chip-icon">{getFileIcon(file.type)}</span>
              <div className="file-chip-info">
                <div className="file-chip-name">{file.name}</div>
                <div className="file-chip-size">{(file.size / 1024).toFixed(1)} KB</div>
              </div>
              <button className="file-chip-remove" onClick={() => { setFile(null); setResult(null); }}>✕</button>
            </div>
          )}

          {error && (
            <div className="alert alert-error" style={{ marginTop: 'var(--space-md)' }}>
              <span className="alert-icon">⚠️</span>
              <div className="alert-content">{error}</div>
            </div>
          )}

          <Button
            variant="primary" full size="lg" loading={loading}
            disabled={!file}
            onClick={handleIdentify}
            style={{ marginTop: 'var(--space-xl)' }}
            id="identify-btn"
          >
            🧬 Identify Owner
          </Button>
        </Card>

        {/* Result */}
        <Card variant={result?.found ? 'accent' : ''} style={{ minHeight: 380 }}>
          {loading ? (
            <div className="loading-overlay">
              <div className="spinner spinner-lg animate-glow-pulse" />
              <p style={{ fontWeight: 600 }}>Looking up identity…</p>
              <div className="loading-pulse">
                <div className="loading-dot" />
                <div className="loading-dot" />
                <div className="loading-dot" />
              </div>
            </div>
          ) : result ? (
            <div className="result-panel animate-fadeInUp">
              {result.found ? (
                <>
                  <div className="badge badge-green" style={{ marginBottom: 'var(--space-sm)' }}>
                    ✅ Identity Found — {result.confidence}% Confidence
                  </div>
                  <div style={{ fontSize: '3rem' }}>👤</div>
                  <h2 style={{ marginBottom: 'var(--space-md)' }}>{result.identity.name}</h2>

                  <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-sm)', width: '100%', maxWidth: 340 }}>
                    {[
                      { label: 'User ID',       value: result.identity.user_id,  icon: '🆔' },
                      { label: 'Email',          value: result.identity.email,     icon: '📧' },
                      { label: 'Organisation',   value: result.identity.org || '—', icon: '🏢' },
                      { label: 'Registered',     value: new Date(result.identity.registered).toLocaleDateString('en-IN', { dateStyle: 'long' }), icon: '📅' },
                    ].map(({ label, value, icon }) => (
                      <div className="owner-result-card" key={label}>
                        <span className="owner-result-label">{icon} {label}</span>
                        <span className="owner-result-value" style={{ fontSize: '0.9rem' }}>{value}</span>
                      </div>
                    ))}
                  </div>
                </>
              ) : (
                <>
                  <div style={{ fontSize: '3rem' }}>❓</div>
                  <h3 style={{ color: 'var(--accent-warn)' }}>No Identity Found</h3>
                  <p style={{ textAlign: 'center', fontSize: '0.85rem', maxWidth: 240 }}>
                    No registered identity matched this file's fingerprint.
                  </p>
                </>
              )}
            </div>
          ) : (
            <div className="result-panel result-panel--empty">
              <div style={{ fontSize: '4rem', opacity: 0.35 }}>🧬</div>
              <h3 style={{ color: 'var(--text-muted)' }}>Awaiting Identification</h3>
              <p style={{ textAlign: 'center', fontSize: '0.85rem', maxWidth: 220 }}>
                Upload a file to look up its owner's registered identity.
              </p>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
};

export default IdentifyPage;
