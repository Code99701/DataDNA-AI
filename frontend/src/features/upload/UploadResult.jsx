import React from 'react';
import Card from '../../components/common/Card';

const UploadResult = ({ result, fileName }) => {
  if (!result) return null;

  return (
    <Card variant="success" style={{ marginTop: 'var(--space-xl)', animation: 'fadeInUp 0.4s ease' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-md)', marginBottom: 'var(--space-lg)' }}>
        <div style={{
          width: 48, height: 48, borderRadius: 'var(--radius-lg)',
          background: 'rgba(16,185,129,0.15)', border: '1px solid rgba(16,185,129,0.3)',
          display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.5rem'
        }}>
          ✅
        </div>
        <div>
          <h3 style={{ color: 'var(--accent-success)', marginBottom: 2 }}>Watermark Embedded!</h3>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: 0 }}>
            Your DataDNA fingerprint is now locked into the file.
          </p>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--space-md)' }}>
        {[
          { label: 'Owner ID',      value: result.owner,        icon: '👤' },
          { label: 'Watermark ID',  value: result.watermark_id, icon: '🔑' },
          { label: 'File',          value: fileName || result.file_name, icon: '📁', span: 2 },
        ].map(({ label, value, icon, span }) => (
          <div key={label} style={{
            gridColumn: span ? `span ${span}` : undefined,
            background: 'rgba(0,0,0,0.25)',
            borderRadius: 'var(--radius-md)',
            padding: 'var(--space-md)',
          }}>
            <div style={{ fontSize: '0.72rem', textTransform: 'uppercase', letterSpacing: '0.1em', color: 'var(--text-muted)', marginBottom: 4 }}>
              {icon} {label}
            </div>
            <div className="code-block" style={{ background: 'transparent', padding: 0, border: 'none', fontSize: '0.9rem' }}>
              {value}
            </div>
          </div>
        ))}
      </div>

      {result.message && (
        <div className="alert alert-info" style={{ marginTop: 'var(--space-md)' }}>
          <span className="alert-icon">ℹ️</span>
          <div className="alert-content">{result.message}</div>
        </div>
      )}
    </Card>
  );
};

export default UploadResult;
