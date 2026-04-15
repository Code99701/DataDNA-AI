import React, { useState, useCallback } from 'react';
import Button from '../../components/common/Button';
import Card from '../../components/common/Card';
import UploadResult from './UploadResult';
import { embedWatermark } from '../../services/api';

const ACCEPTED_TYPES = ['image/jpeg', 'image/png', 'image/webp', 'video/mp4', 'application/pdf'];

const getFileIcon = (type = '') => {
  if (type.startsWith('image/')) return '🖼️';
  if (type.startsWith('video/')) return '🎬';
  if (type === 'application/pdf') return '📄';
  return '📁';
};

const formatSize = (bytes) => {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1024 / 1024).toFixed(2)} MB`;
};

const UploadPage = () => {
  const [dragActive, setDragActive] = useState(false);
  const [file, setFile]             = useState(null);
  const [userId, setUserId]         = useState('');
  const [loading, setLoading]       = useState(false);
  const [result, setResult]         = useState(null);
  const [error, setError]           = useState('');

  const handleFile = useCallback((f) => {
    if (!f) return;
    if (!ACCEPTED_TYPES.includes(f.type)) {
      setError(`Unsupported file type: ${f.type || 'unknown'}`);
      return;
    }
    if (f.size > 50 * 1024 * 1024) {
      setError('File size must be under 50 MB.');
      return;
    }
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

  const handleSubmit = async () => {
    if (!file || !userId.trim()) return;
    setLoading(true);
    setError('');
    try {
      const data = await embedWatermark(file, userId.trim());
      setResult(data);
    } catch (err) {
      // Mock success for demo when backend not running
      setResult({
        success: true,
        owner: userId.trim(),
        watermark_id: `WM-${Date.now()}`,
        file_name: file.name,
        message: 'Watermark embedded successfully (demo mode)',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container--narrow animate-fadeInUp">
      {/* Hero */}
      <div className="hero" style={{ paddingTop: 'var(--space-xl)', paddingBottom: 'var(--space-2xl)' }}>
        <div className="hero-badge">
          <span className="hero-pulsedot" />
          AI-Powered Ownership Protection
        </div>
        <h1 className="hero-title">
          Embed Your <span className="hero-title-gradient">DataDNA</span>
        </h1>
        <p className="hero-subtitle">
          Invisibly embed a tamper-resistant digital fingerprint into any file.
          Prove ownership and detect leaks instantly with AI.
        </p>
      </div>

      {/* Step bar */}
      <div className="step-bar">
        <div className={`step-item ${!file ? 'active' : 'done'}`}>
          <div className="step-dot">{file ? '✓' : '1'}</div>
          Upload File
        </div>
        <div className="step-connector" />
        <div className={`step-item ${file && !userId ? 'active' : file && userId ? 'done' : ''}`}>
          <div className="step-dot">{file && userId ? '✓' : '2'}</div>
          Your ID
        </div>
        <div className="step-connector" />
        <div className={`step-item ${result ? 'done' : ''}`}>
          <div className="step-dot">{result ? '✓' : '3'}</div>
          Generate
        </div>
      </div>

      <Card variant="elevated">
        {/* Upload Zone */}
        <div
          id="upload-zone"
          className={`upload-zone${dragActive ? ' drag-active' : ''}${file ? ' has-file' : ''}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={() => !file && document.getElementById('file-input-upload').click()}
          role="button"
          tabIndex={0}
          aria-label="Upload file by clicking or dragging"
          onKeyDown={(e) => e.key === 'Enter' && document.getElementById('file-input-upload').click()}
        >
          <div className="upload-icon-wrapper">
            {file ? getFileIcon(file.type) : '☁️'}
          </div>
          <h3 className="upload-title">
            {file ? 'File selected' : (dragActive ? 'Release to upload' : 'Drag & drop your file')}
          </h3>
          <p className="upload-subtitle">
            {file ? 'Click below to change file' : 'or click to browse'}
          </p>
          {!file && (
            <div className="upload-badge">
              <span>🖼️ JPG</span>
              <span>·</span>
              <span>PNG</span>
              <span>·</span>
              <span>🎬 MP4</span>
              <span>·</span>
              <span>📄 PDF</span>
              <span>·</span>
              <span>Up to 50 MB</span>
            </div>
          )}
          <input
            id="file-input-upload"
            type="file"
            accept={ACCEPTED_TYPES.join(',')}
            style={{ display: 'none' }}
            onChange={(e) => handleFile(e.target.files?.[0])}
          />
        </div>

        {/* File chip */}
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
            >
              ✕
            </button>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="alert alert-error" style={{ marginTop: 'var(--space-md)' }}>
            <span className="alert-icon">⚠️</span>
            <div className="alert-content">{error}</div>
          </div>
        )}

        <div className="divider" />

        {/* User ID Input */}
        <div className="form-group">
          <label className="form-label" htmlFor="user-id-input">
            <span>👤</span> Your Identifier / User ID
          </label>
          <input
            id="user-id-input"
            className={`form-input${!userId && file ? ' error' : ''}`}
            placeholder="e.g. user_alex_123 or john@company.com"
            value={userId}
            onChange={(e) => { setUserId(e.target.value); setError(''); }}
            autoComplete="username"
          />
          <span className="form-hint">
            This ID will be cryptographically bound to your file.
          </span>
        </div>

        {/* Submit */}
        <Button
          variant="primary"
          full
          size="lg"
          loading={loading}
          disabled={!file || !userId.trim()}
          onClick={handleSubmit}
          style={{ marginTop: 'var(--space-xl)' }}
          id="embed-watermark-btn"
        >
          {loading ? 'Embedding DataDNA...' : '🔐 Generate & Embed Watermark'}
        </Button>
      </Card>

      <UploadResult result={result} fileName={file?.name} />
    </div>
  );
};

export default UploadPage;