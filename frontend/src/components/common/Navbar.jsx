import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navbar = () => {
  const location = useLocation();
  
  return (
    <nav className="navbar">
      <div className="nav-brand">DataDNA AI</div>
      <ul className="nav-links">
        <li>
          <Link to="/" className={location.pathname === '/' ? 'active' : ''}>Home</Link>
        </li>
        <li>
          <Link to="/dashboard" className={location.pathname === '/dashboard' ? 'active' : ''}>Detect Leak</Link>
        </li>
        <li>
          <Link to="/register" className={location.pathname === '/register' ? 'active' : ''}>Register</Link>
        </li>
        <li>
          <Link to="/identify" className={location.pathname === '/identify' ? 'active' : ''}>Identify</Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
