import React from 'react';

/**
 * Button component with multiple variants and states.
 * @param {string} variant - 'primary' | 'secondary' | 'danger' | 'ghost'
 * @param {string} size    - 'sm' | 'md' | 'lg'
 * @param {boolean} loading - shows spinner
 * @param {boolean} full    - full width
 */
const Button = ({
  children,
  variant = 'primary',
  size = 'md',
  loading = false,
  full = false,
  className = '',
  disabled,
  ...props
}) => {
  const classes = [
    'btn',
    `btn-${variant}`,
    size !== 'md' ? `btn-${size}` : '',
    full ? 'btn-full' : '',
    loading ? 'btn-loading' : '',
    className,
  ].filter(Boolean).join(' ');

  return (
    <button className={classes} disabled={disabled || loading} {...props}>
      {loading && <span className="btn-spinner" aria-hidden="true" />}
      {children}
    </button>
  );
};

export default Button;