import { Share2, Clock, CheckCircle2, Copy, Trash2 } from 'lucide-react';
import './ShareRoute.css';

export default function ShareRoute() {
  return (
    <div className="share-route-container">
      <header className="share-header">
        <h1>Share Records</h1>
        <p>Generate secure links to share your medical records with doctors</p>
      </header>

      <section className="share-card">
        <div className="share-card-header">
          <Share2 size={24} color="#3b82f6" />
          <h2>Generate Share Link</h2>
        </div>
        <p>Create a time-limited link to share your complete medical history</p>

        <div className="form-group">
          <label htmlFor="expiry">Link Expiry</label>
          <select id="expiry" defaultValue="48">
            <option value="24">24 hours</option>
            <option value="48">48 hours</option>
            <option value="72">72 hours</option>
            <option value="168">7 days</option>
          </select>
        </div>

        <button className="generate-btn">
          <Share2 size={18} />
          Generate Secure Link
        </button>
      </section>

      <h2 className="section-title">Active Links</h2>
      <div className="active-links-list">
        
        {/* Link 1 */}
        <div className="active-link-wrapper">
          <div className="active-link-left">
            <div className="link-tags-row">
              <span className="link-id">...bc123xyz</span>
              <span className="badge expired">Expired</span>
              <span className="badge viewed">
                <CheckCircle2 size={12} />
                Viewed
              </span>
            </div>
            <div className="expiry-text">
              <Clock size={14} />
              Expires: 1/20/2024
            </div>
          </div>
          <div className="active-link-right">
            <button className="action-icon-btn btn-copy" aria-label="Copy link">
              <Copy size={16} />
            </button>
            <button className="action-icon-btn btn-trash" aria-label="Delete link">
              <Trash2 size={16} />
            </button>
          </div>
        </div>

        {/* Link 2 */}
        <div className="active-link-wrapper">
          <div className="active-link-left">
            <div className="link-tags-row">
              <span className="link-id">...ef456uvw</span>
              <span className="badge expired">Expired</span>
            </div>
            <div className="expiry-text">
              <Clock size={14} />
              Expires: 1/25/2024
            </div>
          </div>
          <div className="active-link-right">
            <button className="action-icon-btn btn-copy" aria-label="Copy link">
              <Copy size={16} />
            </button>
            <button className="action-icon-btn btn-trash" aria-label="Delete link">
              <Trash2 size={16} />
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}
