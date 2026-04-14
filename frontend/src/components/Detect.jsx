import React, { useState } from 'react';

const Detect = ({ onDetect, isProcessing }) => {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
      <div 
        className="upload-zone"
        style={{ padding: '3rem 1rem', borderColor: isProcessing ? 'var(--accent)' : '' }}
        onClick={() => !isProcessing && document.getElementById('detect-upload').click()}
      >
        {isProcessing ? (
          <div className="pulse">
            <div className="upload-icon" style={{ background: 'var(--accent)' }}></div>
            <h3 style={{ color: 'var(--accent)' }}>Extracting DNA...</h3>
          </div>
        ) : (
          <>
            <div className="upload-icon"></div>
            <h3 className="upload-title">{file ? file.name : 'Select file to scan'}</h3>
            <p className="upload-subtitle">Upload the leaked file for analysis</p>
          </>
        )}
        <input 
          id="detect-upload" 
          type="file" 
          style={{ display: 'none' }} 
          onChange={handleFileChange}
          disabled={isProcessing}
        />
      </div>
      
      {file && !isProcessing && (
        <button 
          className="btn-primary" 
          style={{ marginTop: '1.5rem', width: '100%' }}
          onClick={() => onDetect(file)}
        >
          Run Detection Sequence
        </button>
      )}
    </div>
  );
};

export default Detect;
