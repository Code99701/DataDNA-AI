import React, { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';

const NAV_ITEMS = [
  { path: '/',         label: 'Embed',    icon: '🔐' },
  { path: '/verify',   label: 'Verify',   icon: '🔍' },
  { path: '/register', label: 'Register', icon: '👤' },
  { path: '/identify', label: 'Identify', icon: '🧬' },
  { path: '/dashboard',label: 'Dashboard',icon: '📊' },
];

const Navbar = () => {
  const location = useLocation();
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', onScroll);
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  return (
    <nav className={`navbar${scrolled ? ' scrolled' : ''}`} role="navigation" aria-label="Main navigation">
      <Link to="/" className="nav-brand" aria-label="DataDNA AI Home">
        <div className="nav-brand-icon" aria-hidden="true">🧬</div>
        <span className="nav-brand-text">DataDNA AI</span>
      </Link>

      <ul className="nav-links" role="list">
        {NAV_ITEMS.map(({ path, label, icon }) => (
          <li key={path}>
            <Link
              to={path}
              className={location.pathname === path ? 'active' : ''}
              aria-current={location.pathname === path ? 'page' : undefined}
            >
              <span className="nav-icon" aria-hidden="true">{icon}</span>
              {label}
            </Link>
          </li>
        ))}
      </ul>
    </nav>
  );
};

export default Navbar;