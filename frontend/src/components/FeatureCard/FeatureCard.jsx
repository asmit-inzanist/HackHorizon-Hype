import React from 'react';
import './FeatureCard.css';

const FeatureCard = ({ icon, title, description, link }) => {
  return (
    <div className="feature-card">
      <div className="feature-card-icon-wrapper">
        {icon || <span className="feature-card-default-icon">✨</span>}
      </div>
      <div className="feature-card-content">
        <h3 className="feature-card-title">{title || "Feature Title"}</h3>
        <p className="feature-card-description">
          {description || "Explore this amazing feature crafted beautifully with a premium dark navy and vibrant blue aesthetic."}
        </p>
      </div>
      <div className="feature-card-footer">
        <a href={link || "#"} className="feature-card-link">
          Learn More
          <span className="feature-card-arrow">→</span>
        </a>
      </div>
    </div>
  );
};

export default FeatureCard;
