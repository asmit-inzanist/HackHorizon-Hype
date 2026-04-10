import { UploadCloud, Pill, Share2, FileText, Activity, TrendingUp } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import './OverviewRoute.css';

export default function OverviewRoute() {
  const navigate = useNavigate();

  const stats = [
    { label: 'Total Records', value: '12', icon: FileText, color: '#3b82f6' },
    { label: 'Medicines Tracked', value: '28', icon: Activity, color: '#10b981' },
    { label: 'Savings Found', value: '₹2,340', icon: TrendingUp, color: '#f59e0b' }
  ];

  const quickActions = [
    { label: 'Upload Prescription', desc: 'Scan & extract medicines', icon: UploadCloud, path: '/dashboard/upload' },
    { label: 'My Medicines', desc: 'View & find alternatives', icon: Pill, path: '/dashboard/medicines' },
    { label: 'Share Records', desc: 'Generate secure links', icon: Share2, path: '/dashboard/share' }
  ];

  const recentRecords = [
    { title: 'Prescription Apollo Hospital', medicines: 3, date: '2024-01-15' },
    { title: 'Manual Entry', medicines: 2, date: '2024-01-12' },
    { title: 'Prescription Max Healthcare', medicines: 5, date: '2024-01-10' }
  ];

  return (
    <div className="overview-route">
      <header className="dashboard-header">
        <h1>Welcome back, Eagar Nandi 👋</h1>
        <p>Manage your prescriptions and find affordable alternatives</p>
      </header>

      <section className="stats-grid">
        {stats.map((stat, i) => (
          <div key={i} className="dashboard-card stat-card">
            <div className="stat-icon-wrapper" style={{ color: stat.color, backgroundColor: `${stat.color}15` }}>
              <stat.icon size={24} />
            </div>
            <div className="stat-info">
              <h3>{stat.value}</h3>
              <span>{stat.label}</span>
            </div>
          </div>
        ))}
      </section>

      <h2 className="section-title">Quick Actions</h2>
      <section className="quick-actions-grid">
        {quickActions.map((action, i) => (
          <button key={i} className="dashboard-card quick-action-card" onClick={() => navigate(action.path)}>
            <div className="action-icon">
              <action.icon size={28} />
            </div>
            <div className="action-text">
              <h4>{action.label}</h4>
              <p>{action.desc}</p>
            </div>
          </button>
        ))}
      </section>

      <h2 className="section-title">Recent Records</h2>
      <section className="dashboard-card records-list">
        {recentRecords.map((rec, i) => (
          <div key={i} className="record-item">
            <div className="record-left">
              <div className="record-icon-wrapper">
                <FileText size={18} />
              </div>
              <span className="record-title">{rec.title}</span>
            </div>
            <div className="record-right">
              <span className="record-badge">{rec.medicines} medicines</span>
              <span className="record-date">{rec.date}</span>
            </div>
          </div>
        ))}
      </section>
    </div>
  );
}
