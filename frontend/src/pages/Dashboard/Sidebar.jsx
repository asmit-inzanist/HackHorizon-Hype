import { NavLink, useNavigate } from 'react-router-dom';
import { LayoutDashboard, UploadCloud, Pill, Share2, User, LogOut, MapPin, X } from 'lucide-react';
import logo from '../../assets/logo.jpeg';
import './Sidebar.css';

export default function Sidebar({ isOpen, onClose }) {
  const navigate = useNavigate();

  const handleSignOut = () => {
    // Send them back to landing page securely
    navigate('/');
  };

  const navItems = [
    { name: 'Dashboard', icon: LayoutDashboard, path: '/dashboard' },
    { name: 'Upload', icon: UploadCloud, path: '/dashboard/upload' },
    { name: 'Medicines', icon: Pill, path: '/dashboard/medicines' },
    { name: 'Share', icon: Share2, path: '/dashboard/share' },
    { name: 'Profile', icon: User, path: '/dashboard/profile' },
    { name: 'Nearby Clinics', icon: MapPin, path: '/dashboard/clinics' },
  ];

  return (
    <>
      <div className={`sidebar-overlay ${isOpen ? 'open' : ''}`} onClick={onClose}></div>
      <aside className={`sidebar ${isOpen ? 'open' : ''}`}>
        <div className="sidebar-header-row">
          <div className="sidebar-logo">
            <img src={logo} alt="Jain-Aikya Logo" />
            <span>Jain-Aikya</span>
          </div>
          <button className="close-sidebar-btn" onClick={onClose}>
            <X size={24} />
          </button>
        </div>

      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <NavLink 
            key={item.name} 
            to={item.path} 
            end={item.path === '/dashboard'}
            onClick={onClose}
            className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}
          >
            <item.icon className="sidebar-icon" size={20} />
            <span>{item.name}</span>
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-footer">
        <button className="sidebar-link sign-out" onClick={handleSignOut}>
          <LogOut className="sidebar-icon" size={20} />
          <span>Sign Out</span>
        </button>
      </div>
    </aside>
    </>
  );
}
