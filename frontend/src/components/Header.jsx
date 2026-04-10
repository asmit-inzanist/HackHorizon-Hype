// src/components/layout/Header.jsx
import { useState } from 'react';
import './Header.css';
import logo from '../assets/logo.jpeg';

export default function Header({ onAuthClick }) {
    return (
        <header className="header">
            <div className="header-inner">
                <div className="navbar-logo-container">
                    <img src={logo} alt="Jan-Aikya Logo" className="navbar-logo" />
                </div>

                <div className="navbar-actions">
                    <button
                        type="button"
                        className="icon-button"
                        aria-label="Login / Signup"
                        onClick={onAuthClick}
                    >
                        👤
                    </button>
                    <button
                        type="button"
                        className="icon-button"
                        aria-label="Settings"
                    >
                        ⚙️
                    </button>
                </div>
            </div>
        </header>
    );
}