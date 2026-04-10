import { User, Droplet, AlertTriangle, Heart, Save } from 'lucide-react';
import './ProfileRoute.css';

export default function ProfileRoute() {
  return (
    <div className="profile-route-container">
      <header className="profile-header">
        <h1>My Profile</h1>
        <p>Manage your medical profile information</p>
      </header>

      <section className="profile-content-wrapper">
        <div className="profile-section-header">
          <div className="profile-avatar">
            <User size={24} color="white" />
          </div>
          <div className="profile-title-text">
            <h2>Personal Information</h2>
            <span>eagarnandi@gmail.com</span>
          </div>
        </div>
        
        <div className="profile-form">
          <div className="form-row two-cols">
            <div className="form-group">
              <label htmlFor="fullName">Full Name</label>
              <input type="text" id="fullName" defaultValue="Eagar Nandi" />
            </div>
            <div className="form-group">
              <label htmlFor="age">Age</label>
              <input type="text" id="age" placeholder="e.g. 35" />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="bloodGroup">
              <Droplet size={16} className="label-icon text-red" />
              Blood Group
            </label>
            <select id="bloodGroup" defaultValue="">
              <option value="" disabled>Select blood group</option>
              <option value="A+">A+</option>
              <option value="A-">A-</option>
              <option value="B+">B+</option>
              <option value="B-">B-</option>
              <option value="O+">O+</option>
              <option value="O-">O-</option>
              <option value="AB+">AB+</option>
              <option value="AB-">AB-</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="allergies">
              <AlertTriangle size={16} className="label-icon text-yellow" />
              Allergies
            </label>
            <input type="text" id="allergies" placeholder="e.g. Penicillin, Aspirin (comma separated)" />
          </div>

          <div className="form-group">
            <label htmlFor="conditions">
              <Heart size={16} className="label-icon text-pink" />
              Chronic Conditions
            </label>
            <input type="text" id="conditions" placeholder="e.g. Diabetes, Hypertension (comma separated)" />
          </div>
        </div>

        <button className="save-profile-btn">
          <Save size={18} />
          Save Profile
        </button>
      </section>
    </div>
  );
}
