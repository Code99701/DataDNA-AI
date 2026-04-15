import React, { useState } from 'react';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import VerifyResult from './VerifyResult';

const VerifyPage = () => {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleDetection = () => {
    if (!file) return;
    setIsProcessing(true);
    setResult(null);
    
    // Simulate AI processing time with a mock timeout
    setTimeout(() => {
      setResult({
        owner: 'user_alex_123',
        confidence: 94
      });
      setIsProcessing(false);
    }, 2500);
  };

  return (
    <div className="dashboard-page">
      <div className="section-header">
        <h1 style={{ fontSize: '2.5rem' }}>Leak Detection</h1>
      </div>
      <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>
        Found a suspicious file? Upload it here to extract its hidden DataDNA and discover the original owner.
      </p>
      
      <div className="dashboard-grid">
        <Card style={{ display: 'flex', flexDirection: 'column' }}>
          <h2 style={{ marginBottom: '1.5rem', fontSize: '1.5rem' }}>Upload Suspicious File</h2>
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
              <Button 
                style={{ marginTop: '1.5rem', width: '100%' }}
                onClick={handleDetection}
              >
                Run Detection Sequence
              </Button>
            )}
          </div>
        </Card>
        
        <Card style={{ background: 'rgba(30, 27, 75, 0.4)' }}>
          <VerifyResult data={result} isProcessing={isProcessing} />
        </Card>
      </div>
    </div>
  );
};

export default VerifyPage;
