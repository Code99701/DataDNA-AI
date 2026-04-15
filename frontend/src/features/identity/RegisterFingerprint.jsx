import React from 'react';
import Card from '../../components/common/Card';

const RegisterPage = () => {
  return (
    <div className="home-page">
      <div className="section-header">
        <h1 style={{ fontSize: '2.5rem' }}>Register Identity</h1>
      </div>
      <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>
        Create your unique digital identity to sign your files with DataDNA.
      </p>
      
      <Card>
        <div style={{ textAlign: 'center', padding: '2rem' }}>
          <h3>Registration form coming soon</h3>
        </div>
      </Card>
    </div>
  );
};

export default RegisterPage;
