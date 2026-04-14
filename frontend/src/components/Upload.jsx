import React, { useState } from 'react';

const Upload = ({ title = "Drag & drop your file here" }) => {
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
    <div>
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
          <button className="btn-primary">Generate & Embed Watermark</button>
        </div>
      )}
    </div>
  );
};

export default Upload;
