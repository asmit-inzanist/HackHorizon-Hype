import { MapPin, Search, Navigation } from 'lucide-react';
import './ClinicsRoute.css';

export default function ClinicsRoute() {
  const clinics = [
    { name: 'City Central Hospital', distance: '1.2 km', waitTime: '15 mins', status: 'Open' },
    { name: 'Sunrise Medicare', distance: '2.5 km', waitTime: '5 mins', status: 'Open' },
    { name: 'Apollo Health Center', distance: '3.8 km', waitTime: '45 mins', status: 'Open' },
  ];

  return (
    <div className="clinics-route-container">
      <header className="clinics-header">
        <h1>Nearby Clinics</h1>
        <p>Find and navigate to healthcare facilities near your location</p>
      </header>

      <div className="clinics-search-container dashboard-card">
        <Search className="search-icon" size={20} />
        <input type="text" className="clinics-search-input" placeholder="Search by name, specialty, or location..." />
      </div>

      <div className="clinics-list">
        {clinics.map((clinic, index) => (
          <div key={index} className="clinic-card dashboard-card">
            <div className="clinic-info">
              <div className="clinic-header">
                <h2>{clinic.name}</h2>
                <span className="status-badge">{clinic.status}</span>
              </div>
              
              <div className="clinic-details">
                <span className="detail-item">
                  <MapPin size={16} />
                  {clinic.distance} away
                </span>
                <span className="detail-item wait-time">
                  Wait time: {clinic.waitTime}
                </span>
              </div>
            </div>
            
            <button className="navigate-btn">
              <Navigation size={18} />
              Directions
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
