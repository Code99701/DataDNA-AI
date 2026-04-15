import React from 'react';
import Card from '../../components/common/Card';

const IdentifyPage = () => {
  return (
    <div className="home-page">
      <div className="section-header">
        <h1 style={{ fontSize: '2.5rem' }}>Identify Identity</h1>
      </div>
      <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>
        Check ownership validity and identify users through DataDNA.
      </p>
      
      <Card>
        <div style={{ textAlign: 'center', padding: '2rem' }}>
          <h3>Identification features coming soon</h3>
        </div>
      </Card>
    </div>
  );
};

export default IdentifyPage;
