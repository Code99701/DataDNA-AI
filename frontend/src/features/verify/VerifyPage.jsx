import React, { useState, useCallback } from 'react';
import Button from '../../components/common/Button';
import Card from '../../components/common/Card';
import VerifyResult from './VerifyResult';
import { verifyFingerprint } from '../../services/api';

const getFileIcon = (type = '') => {
  if (type.startsWith('image/')) return '🖼️';
  if (type.startsWith('video/')) return '🎬';
  if (type === 'application/pdf') return '📄';
  return '📁';
};

const formatSize = (bytes) => {
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1024 / 1024).toFixed(2)} MB`;
};

const VerifyPage = () => {
  const [dragActive, setDragActive] = useState(false);
  const [file, setFile]             = useState(null);
  const [loading, setLoading]       = useState(false);
  const [result, setResult]         = useState(null);
  const [error, setError]           = useState('');

  const handleFile = useCallback((f) => {
    if (!f) return;
    setError('');
    setResult(null);
    setFile(f);
  }, []);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(e.type === 'dragenter' || e.type === 'dragover');
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    handleFile(e.dataTransfer.files?.[0]);
  };

  const handleDetect = async () => {
    if (!file) return;
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const data = await verifyFingerprint(file);
      setResult(data);
    } catch (err) {
      // Mock result for demo
      await new Promise(r => setTimeout(r, 2200));
      setResult({
        found: true,
        owner: 'user_alex_123',
        confidence: 94,
        watermark_id: 'WM-1712345678901',
        embed_date: '2026-04-14T08:30:00Z',
        file_name: file.name,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container animate-fadeInUp">
      {/* Header */}
      <div className="section-header">
        <div className="section-title">
          <span className="section-eyebrow">🔍 Leak Detection</span>
          <h1>Verify File Ownership</h1>
          <p style={{ maxWidth: 520, marginTop: 'var(--space-sm)' }}>
            Found a suspicious file? Upload it to extract the hidden DataDNA
            fingerprint and identify the original owner instantly.
          </p>
        </div>
      </div>

      <div className="dashboard-split">
        {/* Left: Upload Panel */}
        <Card variant="elevated">
          <h2 style={{ fontSize: '1.2rem', marginBottom: 'var(--space-xl)' }}>
            📤 Upload Suspicious File
          </h2>

          {loading ? (
            <div className="loading-overlay">
              <div className="spinner spinner-lg animate-glow-pulse" />
              <div>
                <p style={{ fontWeight: 600, textAlign: 'center' }}>Extracting DataDNA…</p>
                <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', textAlign: 'center', marginTop: 4 }}>
                  Running deep autoencoder analysis
                </p>
              </div>
              <div className="loading-pulse">
                <div className="loading-dot" />
                <div className="loading-dot" />
                <div className="loading-dot" />
              </div>
            </div>
          ) : (
            <>
              <div
                className={`upload-zone${dragActive ? ' drag-active' : ''}${file ? ' has-file' : ''}`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
                onClick={() => !file && document.getElementById('verify-file-input').click()}
                role="button"
                tabIndex={0}
                aria-label="Upload suspicious file"
                onKeyDown={(e) => e.key === 'Enter' && document.getElementById('verify-file-input').click()}
              >
                <div className="upload-icon-wrapper">
                  {file ? getFileIcon(file.type) : '🔎'}
                </div>
                <h3 className="upload-title">
                  {file ? 'File ready for scanning' : dragActive ? 'Drop to scan' : 'Select file to scan'}
                </h3>
                <p className="upload-subtitle">
                  {file ? file.name : 'Drag & drop or click to browse'}
                </p>
                <input
                  id="verify-file-input"
                  type="file"
                  style={{ display: 'none' }}
                  onChange={(e) => handleFile(e.target.files?.[0])}
                />
              </div>

              {file && (
                <div className="file-chip">
                  <span className="file-chip-icon">{getFileIcon(file.type)}</span>
                  <div className="file-chip-info">
                    <div className="file-chip-name">{file.name}</div>
                    <div className="file-chip-size">{formatSize(file.size)}</div>
                  </div>
                  <button
                    className="file-chip-remove"
                    onClick={() => { setFile(null); setResult(null); }}
                    aria-label="Remove file"
                  >✕</button>
                </div>
              )}

              {error && (
                <div className="alert alert-error" style={{ marginTop: 'var(--space-md)' }}>
                  <span className="alert-icon">⚠️</span>
                  <div className="alert-content">{error}</div>
                </div>
              )}

              <Button
                variant="primary"
                full
                size="lg"
                loading={loading}
                disabled={!file}
                onClick={handleDetect}
                style={{ marginTop: 'var(--space-xl)' }}
                id="run-detection-btn"
              >
                🧬 Run Detection Sequence
              </Button>
            </>
          )}
        </Card>

        {/* Right: Result Panel */}
        <Card variant={result?.found ? 'accent' : ''} style={{ minHeight: 380 }}>
          <VerifyResult result={result} loading={loading} />
        </Card>
      </div>
    </div>
  );
};

export default VerifyPage;