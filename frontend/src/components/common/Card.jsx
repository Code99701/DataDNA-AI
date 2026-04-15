import React from 'react';

/**
 * Reusable Card / glass panel component.
 * @param {string} variant - '' | 'elevated' | 'accent' | 'danger' | 'success'
 */
const Card = ({ children, variant = '', className = '', ...props }) => {
  const classes = [
    'card',
    variant ? `card--${variant}` : '',
    className,
  ].filter(Boolean).join(' ');

  return (
    <div className={classes} {...props}>
      {children}
    </div>
  );
};

export default Card;