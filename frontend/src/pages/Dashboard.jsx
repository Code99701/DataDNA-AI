import React, { useState } from 'react';
import Detect from '../components/Detect';
import Result from '../components/Result';

const Dashboard = () => {
  const [result, setResult] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);

  // Mock processing logic to demonstrate UI
  const handleDetection = (file) => {
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
        <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column' }}>
          <h2 style={{ marginBottom: '1.5rem', fontSize: '1.5rem' }}>Upload Suspicious File</h2>
          <Detect onDetect={handleDetection} isProcessing={isProcessing} />
        </div>
        
        <div className="glass-panel" style={{ background: 'rgba(30, 27, 75, 0.4)' }}>
          <Result data={result} isProcessing={isProcessing} />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
