import React from 'react';
import './Header.css';

function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <h1>🔐 Quantum Key Distribution Simulator</h1>
        <p className="subtitle">
          Educational tool for simulating BB84, B92, E91, and BBM92 protocols
        </p>
      </div>
    </header>
  );
}

export default Header;
