import React, { useState } from 'react';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import UploadResult from './UploadResult';

const UploadPage = ({ title = "Drag & drop your file here to secure it" }) => {
  const [dragActive, setDragActive] = useState(false);
  const [file, setFile] = useState(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  return (
    <div className="home-page">
      <section className="hero">
        <h1>Secure Your Digital Ownership</h1>
        <p>
          DataDNA AI embeds a hidden, tamper-resistant fingerprint into your files. 
          Protect your assets against leaks and unauthorized sharing with state-of-the-art AI autoencoders.
        </p>
      </section>

      <section id="upload-section">
        <Card>
          <div className="section-header">
            <h2 style={{ fontSize: '2rem' }}>New Upload</h2>
          </div>
          <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>
            Upload a file to inject a unique DataDNA fingerprint. The processed file will be yours mathematically.
          </p>
          
          <div 
            className={`upload-zone ${dragActive ? 'drag-active' : ''}`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            onClick={() => document.getElementById('file-upload').click()}
          >
            <div className="upload-icon"></div>
            <h3 className="upload-title">{file ? file.name : title}</h3>
            <p className="upload-subtitle">
              {file ? `Size: ${(file.size / 1024 / 1024).toFixed(2)} MB` : 'Supports JPG, PNG, MP4 up to 50MB'}
            </p>
            <input 
              id="file-upload" 
              type="file" 
              style={{ display: 'none' }} 
              onChange={handleChange}
            />
          </div>
          
          {file && (
            <div style={{ marginTop: '1.5rem', textAlign: 'center' }}>
               <Button>Generate & Embed Watermark</Button>
            </div>
          )}
          <UploadResult file={file} />
        </Card>
      </section>
    </div>
  );
};

export default UploadPage;
