/*
 * Talk-Less Header Component
 * Copyright (C) 2024 Talk-Less Contributors
 * Licensed under AGPL-3.0-or-later
 */

import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Header.css';

function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();

  const toggleMobileMenu = () => {
    setMobileMenuOpen(!mobileMenuOpen);
  };

  const isActive = (path) => {
    return location.pathname === path ? 'active' : '';
  };

  return (
    <header className="header no-print">
      <div className="header-container">
        <div className="header-brand">
          <Link to="/" className="header-logo">
            <h1>Talk-Less</h1>
          </Link>
          <p className="header-tagline">Transparent News Aggregation</p>
        </div>

        <button
          className="mobile-menu-toggle"
          onClick={toggleMobileMenu}
          aria-label="Toggle navigation menu"
          aria-expanded={mobileMenuOpen}
        >
          <span className="hamburger-line"></span>
          <span className="hamburger-line"></span>
          <span className="hamburger-line"></span>
        </button>

        <nav className={`header-nav ${mobileMenuOpen ? 'mobile-open' : ''}`}>
          <ul className="nav-list">
            <li>
              <Link
                to="/"
                className={isActive('/')}
                onClick={() => setMobileMenuOpen(false)}
              >
                Home
              </Link>
            </li>
            <li>
              <Link
                to="/sources"
                className={isActive('/sources')}
                onClick={() => setMobileMenuOpen(false)}
              >
                Sources
              </Link>
            </li>
            <li>
              <Link
                to="/transparency"
                className={isActive('/transparency')}
                onClick={() => setMobileMenuOpen(false)}
              >
                Transparency
              </Link>
            </li>
            <li>
              <Link
                to="/about"
                className={isActive('/about')}
                onClick={() => setMobileMenuOpen(false)}
              >
                About
              </Link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
}

export default Header;
