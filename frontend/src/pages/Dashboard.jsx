import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Card from '../components/common/Card';
import Button from '../components/common/Button';

const STATS = [
  {
    id: 'total-files',
    icon: '📁', label: 'Files Protected', value: '2,841',
    delta: '+128 this week', color: '#8b5cf6',
    bg: 'rgba(139,92,246,0.12)',
  },
  {
    id: 'leaks-detected',
    icon: '🔍', label: 'Leaks Detected', value: '47',
    delta: '+3 today', color: '#06b6d4',
    bg: 'rgba(6,182,212,0.12)',
  },
  {
    id: 'identities',
    icon: '👤', label: 'Identities', value: '312',
    delta: '+12 this month', color: '#10b981',
    bg: 'rgba(16,185,129,0.12)',
  },
  {
    id: 'accuracy',
    icon: '🎯', label: 'Avg. Accuracy', value: '96.4%',
    delta: 'All-time high', color: '#f59e0b',
    bg: 'rgba(245,158,11,0.12)',
  },
];

const RECENT_ACTIVITY = [
  { id: 1, type: 'embed',    file: 'product_photo_v3.png',    user: 'user_alex_123',  time: '2 min ago',   status: 'success' },
  { id: 2, type: 'detect',   file: 'leaked_report_2026.pdf', user: 'user_maria_007', time: '18 min ago',  status: 'found'   },
  { id: 3, type: 'identify', file: 'promo_video_final.mp4',  user: 'user_jay_99',    time: '1 hr ago',    status: 'success' },
  { id: 4, type: 'embed',    file: 'design_asset_v7.jpg',    user: 'user_alex_123',  time: '3 hrs ago',   status: 'success' },
  { id: 5, type: 'detect',   file: 'confidential_deck.pptx', user: 'user_priya_42',  time: 'Yesterday',   status: 'not_found'},
];

const TYPE_CONFIG = {
  embed:    { icon: '🔐', label: 'Embed',    badge: 'badge-purple' },
  detect:   { icon: '🔍', label: 'Detect',   badge: 'badge-cyan'   },
  identify: { icon: '🧬', label: 'Identify', badge: 'badge-green'  },
};

const STATUS_CONFIG = {
  success:   { icon: '✅', badge: 'badge-green', label: 'Success'   },
  found:     { icon: '🔎', badge: 'badge-cyan',  label: 'Found'     },
  not_found: { icon: '❓', badge: 'badge-amber', label: 'Not Found' },
};

const Dashboard = () => {
  const [animatedValues, setAnimatedValues] = useState(STATS.map(() => 0));

  useEffect(() => {
    // Staggered counter animation
    STATS.forEach((stat, i) => {
      const numericVal = parseFloat(stat.value.replace(/[^0-9.]/g, ''));
      if (isNaN(numericVal)) return;
      const duration = 1200;
      const steps = 50;
      const stepVal = numericVal / steps;
      let current = 0;
      const timer = setInterval(() => {
        current = Math.min(current + stepVal, numericVal);
        setAnimatedValues(prev => {
          const next = [...prev];
          next[i] = current;
          return next;
        });
        if (current >= numericVal) clearInterval(timer);
      }, duration / steps);
    });
  }, []);

  const formatAnimated = (val, stat) => {
    if (stat.value.includes('%')) return `${val.toFixed(1)}%`;
    if (val >= 1000) return `${(val / 1000).toFixed(1)}k`;
    return Math.floor(val).toString();
  };

  return (
    <div className="page-container animate-fadeInUp">
      {/* Header */}
      <div className="section-header">
        <div className="section-title">
          <span className="section-eyebrow">📊 Overview</span>
          <h1>Dashboard</h1>
          <p style={{ marginTop: 'var(--space-sm)' }}>
            Realtime overview of your DataDNA protection system.
          </p>
        </div>
        <div style={{ display: 'flex', gap: 'var(--space-md)', flexWrap: 'wrap' }}>
          <Button variant="ghost" size="sm" id="refresh-stats-btn">🔄 Refresh</Button>
          <Link to="/" className="btn btn-primary btn-sm" id="go-embed-btn">🔐 New Embed</Link>
        </div>
      </div>

      {/* Stat Cards */}
      <div className="stats-grid">
        {STATS.map((stat, i) => (
          <div className="stat-card" key={stat.id} id={`stat-card-${stat.id}`}>
            <div className="stat-card-header">
              <div className="stat-card-icon" style={{ background: stat.bg }}>
                {stat.icon}
              </div>
              <div className="badge badge-green" style={{ fontSize: '0.7rem' }}>Live</div>
            </div>
            <div>
              <div className="stat-card-value" style={{ color: stat.color }}>
                {formatAnimated(animatedValues[i], stat)}
              </div>
              <div className="stat-card-label">{stat.label}</div>
            </div>
            <div className="stat-card-delta">↑ {stat.delta}</div>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <h2 style={{ fontSize: '1.15rem', marginBottom: 'var(--space-lg)' }}>⚡ Quick Actions</h2>
      <div className="feature-grid" style={{ marginBottom: 'var(--space-2xl)' }}>
        {[
          { to: '/',         icon: '🔐', title: 'Embed Watermark', desc: 'Protect a new file with your DataDNA signature.',        color: '#8b5cf6' },
          { to: '/verify',   icon: '🔍', title: 'Verify / Detect', desc: 'Check if a file contains a watermark and find its owner.', color: '#06b6d4' },
          { to: '/register', icon: '👤', title: 'Register Identity', desc: 'Create your cryptographic digital identity.',           color: '#10b981' },
          { to: '/identify', icon: '🧬', title: 'Identify Author',  desc: 'Look up the registered owner of any file.',               color: '#f59e0b' },
        ].map(({ to, icon, title, desc, color }) => (
          <Link
            key={to}
            to={to}
            style={{ textDecoration: 'none' }}
            id={`quick-action-${title.toLowerCase().replace(/\s+/g, '-')}`}
          >
            <div className="feature-card" style={{ cursor: 'pointer' }}>
              <div className="feature-card-icon" style={{ background: `${color}20`, borderColor: `${color}40`, color }}>
                {icon}
              </div>
              <div className="feature-card-title">{title}</div>
              <div className="feature-card-desc">{desc}</div>
            </div>
          </Link>
        ))}
      </div>

      {/* Recent Activity */}
      <h2 style={{ fontSize: '1.15rem', marginBottom: 'var(--space-lg)' }}>🕒 Recent Activity</h2>
      <Card variant="elevated">
        <div style={{ display: 'flex', flexDirection: 'column', gap: 0 }}>
          {RECENT_ACTIVITY.map((item, idx) => {
            const type   = TYPE_CONFIG[item.type];
            const status = STATUS_CONFIG[item.status];
            return (
              <div
                key={item.id}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 'var(--space-md)',
                  padding: 'var(--space-md) var(--space-lg)',
                  borderBottom: idx < RECENT_ACTIVITY.length - 1 ? '1px solid var(--border)' : 'none',
                  transition: 'background var(--transition-fast)',
                  borderRadius: idx === 0 ? 'var(--radius-lg) var(--radius-lg) 0 0' : idx === RECENT_ACTIVITY.length - 1 ? '0 0 var(--radius-lg) var(--radius-lg)' : 0,
                }}
                onMouseEnter={e => e.currentTarget.style.background = 'rgba(255,255,255,0.03)'}
                onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
              >
                <div style={{
                  width: 38, height: 38, borderRadius: 'var(--radius-md)',
                  background: 'rgba(255,255,255,0.06)', display: 'flex',
                  alignItems: 'center', justifyContent: 'center', fontSize: '1.1rem',
                  flexShrink: 0,
                }}>
                  {type.icon}
                </div>
                <div style={{ flex: 1, overflow: 'hidden' }}>
                  <div style={{ fontWeight: 600, fontSize: '0.88rem', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    {item.file}
                  </div>
                  <div style={{ fontSize: '0.77rem', color: 'var(--text-muted)', marginTop: 2 }}>
                    by {item.user}
                  </div>
                </div>
                <span className={`badge ${type.badge}`} style={{ flexShrink: 0 }}>{type.label}</span>
                <span className={`badge ${status.badge}`} style={{ flexShrink: 0 }}>{status.icon} {status.label}</span>
                <span style={{ fontSize: '0.77rem', color: 'var(--text-muted)', flexShrink: 0, minWidth: 70, textAlign: 'right' }}>
                  {item.time}
                </span>
              </div>
            );
          })}
        </div>
      </Card>
    </div>
  );
};

export default Dashboard;