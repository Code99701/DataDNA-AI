import React, { useState } from 'react';
import Button from '../../components/common/Button';
import Card from '../../components/common/Card';
import { registerIdentity } from '../../services/api';

const RegisterPage = () => {
  const [form, setForm] = useState({ name: '', email: '', userId: '', org: '' });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(null);

  const validate = () => {
    const e = {};
    if (!form.name.trim())   e.name   = 'Full name is required';
    if (!form.email.trim())  e.email  = 'Email is required';
    else if (!/\S+@\S+\.\S+/.test(form.email)) e.email = 'Invalid email address';
    if (!form.userId.trim()) e.userId = 'User ID is required';
    return e;
  };

  const handleChange = (field) => (e) => {
    setForm(f => ({ ...f, [field]: e.target.value }));
    setErrors(er => ({ ...er, [field]: '' }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const errs = validate();
    if (Object.keys(errs).length) { setErrors(errs); return; }
    setLoading(true);
    try {
      const data = await registerIdentity(form);
      setSuccess(data);
    } catch {
      // Mock for demo
      setSuccess({
        identity_id: `ID-${Date.now()}`,
        user_id: form.userId,
        email: form.email,
        name: form.name,
        created_at: new Date().toISOString(),
      });
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="page-container--narrow animate-fadeInUp">
        <Card variant="success" style={{ textAlign: 'center', padding: 'var(--space-3xl)' }}>
          <div style={{ fontSize: '4rem', marginBottom: 'var(--space-lg)' }}>🎉</div>
          <h2 style={{ color: 'var(--accent-success)', marginBottom: 'var(--space-md)' }}>
            Identity Registered!
          </h2>
          <p style={{ color: 'var(--text-secondary)', marginBottom: 'var(--space-xl)' }}>
            Your digital identity is now active. You can start embedding DataDNA into your files.
          </p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-md)', textAlign: 'left' }}>
            {[
              { label: 'Identity ID', value: success.identity_id, icon: '🆔' },
              { label: 'User ID',     value: success.user_id,     icon: '👤' },
              { label: 'Email',       value: success.email,        icon: '📧' },
            ].map(({ label, value, icon }) => (
              <div key={label} className="owner-result-card">
                <span className="owner-result-label">{icon} {label}</span>
                <span className="owner-result-value" style={{ fontSize: '0.95rem' }}>{value}</span>
              </div>
            ))}
          </div>
          <Button
            variant="secondary"
            style={{ marginTop: 'var(--space-xl)' }}
            onClick={() => { setSuccess(null); setForm({ name: '', email: '', userId: '', org: '' }); }}
          >
            Register Another
          </Button>
        </Card>
      </div>
    );
  }

  return (
    <div className="page-container--narrow animate-fadeInUp">
      <div className="hero" style={{ paddingTop: 'var(--space-xl)', paddingBottom: 'var(--space-2xl)' }}>
        <div className="hero-badge">
          <span className="hero-pulsedot" />
          Secure Identity System
        </div>
        <h1 className="hero-title">
          Register Your <span className="hero-title-gradient">Identity</span>
        </h1>
        <p className="hero-subtitle">
          Create your cryptographic digital identity to sign files and prove ownership on the DataDNA network.
        </p>
      </div>

      <Card variant="elevated">
        <form onSubmit={handleSubmit} noValidate>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--space-lg)' }}>
            <div className="form-group" style={{ gridColumn: 'span 2' }}>
              <label className="form-label" htmlFor="reg-name">Full Name *</label>
              <input
                id="reg-name"
                className={`form-input${errors.name ? ' error' : ''}`}
                placeholder="Alex Johnson"
                value={form.name}
                onChange={handleChange('name')}
                autoComplete="name"
              />
              {errors.name && <div className="form-error">⚠️ {errors.name}</div>}
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="reg-email">Email *</label>
              <input
                id="reg-email"
                type="email"
                className={`form-input${errors.email ? ' error' : ''}`}
                placeholder="alex@example.com"
                value={form.email}
                onChange={handleChange('email')}
                autoComplete="email"
              />
              {errors.email && <div className="form-error">⚠️ {errors.email}</div>}
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="reg-userId">User ID *</label>
              <input
                id="reg-userId"
                className={`form-input${errors.userId ? ' error' : ''}`}
                placeholder="user_alex_123"
                value={form.userId}
                onChange={handleChange('userId')}
                autoComplete="username"
              />
              {errors.userId && <div className="form-error">⚠️ {errors.userId}</div>}
              <span className="form-hint">Unique identifier for your watermarks.</span>
            </div>

            <div className="form-group" style={{ gridColumn: 'span 2' }}>
              <label className="form-label" htmlFor="reg-org">Organisation (optional)</label>
              <input
                id="reg-org"
                className="form-input"
                placeholder="ACME Corp"
                value={form.org}
                onChange={handleChange('org')}
                autoComplete="organization"
              />
            </div>
          </div>

          <div className="divider" />

          <Button
            variant="primary" full size="lg" loading={loading}
            id="register-identity-btn"
          >
            👤 Create Digital Identity
          </Button>
        </form>
      </Card>

      {/* Info cards */}
      <div className="feature-grid" style={{ marginTop: 'var(--space-2xl)' }}>
        {[
          { icon: '🔐', title: 'Cryptographically Secure', desc: 'Your identity is tied to your files using AI-generated embeddings.' },
          { icon: '🌐', title: 'Global Lookup',           desc: 'Any DataDNA user can verify your ownership claim globally.' },
          { icon: '⚡', title: 'Instant Verification',    desc: 'Ownership proof is extracted in under a second from any copy.' },
        ].map(({ icon, title, desc }) => (
          <div className="feature-card" key={title}>
            <div className="feature-card-icon">{icon}</div>
            <div className="feature-card-title">{title}</div>
            <div className="feature-card-desc">{desc}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RegisterPage;
