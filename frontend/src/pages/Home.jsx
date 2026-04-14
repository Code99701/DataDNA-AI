import React from 'react';
import { Link } from 'react-router-dom';
import Upload from '../components/Upload';

const Home = () => {
  return (
    <div className="home-page">
      <section className="hero">
        <h1>Secure Your Digital Ownership</h1>
        <p>
          DataDNA AI embeds a hidden, tamper-resistant fingerprint into your files. 
          Protect your assets against leaks and unauthorized sharing with state-of-the-art AI autoencoders.
        </p>
        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', marginBottom: '4rem' }}>
          <a href="#upload-section" className="btn-primary">Embed Watermark</a>
          <Link to="/dashboard" className="btn-secondary">Check File Status</Link>
        </div>
      </section>

      <section id="upload-section" className="glass-panel">
        <div className="section-header">
          <h2 style={{ fontSize: '2rem' }}>New Upload</h2>
        </div>
        <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>
          Upload a file to inject a unique DataDNA fingerprint. The processed file will be yours mathematically.
        </p>
        <Upload title="Drag & drop your file here to secure it" />
      </section>
    </div>
  );
};

export default Home;
