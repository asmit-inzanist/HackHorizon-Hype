import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Authbox.css';

export default function AuthBox() {
  const navigate = useNavigate();
  const [mode, setMode] = useState('login'); // 'login' | 'signup'
  const isLogin = mode === 'login';

  const [form, setForm] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
  });

  function handleChange(e) {
    const { name, value } = e.target;
    setForm(prev => ({ ...prev, [name]: value }));
  }

  function handleSubmit(e) {
    e.preventDefault();
    if (isLogin) {
      console.log('login', form.email, form.password);
      navigate('/dashboard');
    } else {
      console.log('signup', form);
      navigate('/dashboard');
    }
  }

  return (
    <div className="auth-box">
      {/* Tabs */}
      <div className="auth-tabs" role="tablist" aria-label="Auth mode">
        <button
          type="button"
          role="tab"
          className={`auth-tab ${isLogin ? 'auth-tab--active' : ''}`}
          aria-selected={isLogin}
          onClick={() => setMode('login')}
        >
          Log in
        </button>
        <button
          type="button"
          role="tab"
          className={`auth-tab ${!isLogin ? 'auth-tab--active' : ''}`}
          aria-selected={!isLogin}
          onClick={() => setMode('signup')}
        >
          Sign up
        </button>
      </div>

      {/* Form */}
      <form className="auth-form" onSubmit={handleSubmit}>
        {!isLogin && (
          <div className="auth-field">
            <label htmlFor="name">Full name</label>
            <input
              id="name"
              name="name"
              type="text"
              autoComplete="name"
              value={form.name}
              onChange={handleChange}
              placeholder="Enter your name"
              required
            />
          </div>
        )}

        <div className="auth-field">
          <label htmlFor="email">Email address</label>
          <input
            id="email"
            name="email"
            type="email"
            autoComplete="email"
            value={form.email}
            onChange={handleChange}
            placeholder="you@example.com"
            required
          />
        </div>

        <div className="auth-field">
          <label htmlFor="password">Password</label>
          <input
            id="password"
            name="password"
            type="password"
            autoComplete={isLogin ? 'current-password' : 'new-password'}
            value={form.password}
            onChange={handleChange}
            placeholder="••••••••"
            required
          />
        </div>

        {!isLogin && (
          <div className="auth-field">
            <label htmlFor="confirmPassword">Confirm password</label>
            <input
              id="confirmPassword"
              name="confirmPassword"
              type="password"
              value={form.confirmPassword}
              onChange={handleChange}
              placeholder="••••••••"
              required
            />
          </div>
        )}

        <button type="submit" className="auth-submit">
          {isLogin ? 'Continue' : 'Create account'}
        </button>
      </form>
    </div>
  );
}