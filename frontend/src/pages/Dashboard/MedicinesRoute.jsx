import { Search, Pill, ArrowUpRight, Info, X, Shield } from 'lucide-react';
import { useState } from 'react';
import './MedicinesRoute.css';

export default function MedicinesRoute() {
  const medicines = [
    { name: 'Crocin 500mg', generic: 'Paracetamol', dosage: '500mg', freq: 'Twice daily' },
    { name: 'Augmentin 625', generic: 'Amoxicillin + Clavulanate', dosage: '625mg', freq: 'Three times daily' },
    { name: 'Pan 40', generic: 'Pantoprazole', dosage: '40mg', freq: 'Once daily' },
    { name: 'Glycomet 500', generic: 'Metformin', dosage: '500mg', freq: 'Twice daily' },
  ];

  const [selectedMed, setSelectedMed] = useState(null);

  const rawAlternatives = [
    { name: 'Dolo 650', mfg: 'Micro Labs', price: 18, originalPrice: 30, savePercent: '40%' },
    { name: 'Calpol 500mg', mfg: 'GSK', price: 22, originalPrice: 30, savePercent: '26.7%' },
    { name: 'Pacimol 650', mfg: 'Ipca Labs', price: 15, originalPrice: 30, savePercent: '50%' }
  ];

  // User requested descending order
  const sortedAlternatives = [...rawAlternatives].sort((a, b) => b.price - a.price);

  return (
    <div className="medicines-route">
      <header className="dashboard-header">
        <h1>My Medicines</h1>
        <p>View extracted medicines and find affordable alternatives</p>
      </header>

      <div className="search-container">
        <Search className="search-icon" size={20} />
        <input type="text" placeholder="Search medicines by name or generic..." className="modern-input search-input" />
      </div>

      <div className="medicines-list">
        {medicines.map((med, i) => (
           <div key={i} className="dashboard-card medicine-card">
              <div className="medicine-left">
                <div className="med-icon-wrapper">
                  <Pill size={20} />
                </div>
                <div className="med-info">
                  <h3>{med.name}</h3>
                  <p>{med.generic}</p>
                  <div className="med-tags">
                    <span className="med-tag dosage">{med.dosage}</span>
                    <span className="med-tag freq">{med.freq}</span>
                  </div>
                </div>
              </div>

              <div className="medicine-right">
                <button className="med-action-btn alt-btn" onClick={() => setSelectedMed(med.name)}>
                   <ArrowUpRight size={16} />
                   Alternatives
                </button>
                <button className="med-action-btn detail-btn">
                   <Info size={16} />
                   Details
                </button>
              </div>
           </div>
        ))}
      </div>

      {selectedMed && (
        <div className="modal-overlay" onClick={() => setSelectedMed(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Alternatives for {selectedMed}</h2>
              <button className="close-modal-btn" onClick={() => setSelectedMed(null)}>
                <X size={20} color="#3b82f6" />
              </button>
            </div>
            
            <div className="alternatives-list">
              {sortedAlternatives.map((alt, idx) => (
                <div key={idx} className="alt-card">
                  <div className="alt-card-left">
                    <h3>{alt.name}</h3>
                    <p>{alt.mfg}</p>
                  </div>
                  <div className="alt-card-right">
                    <div className="price-row">
                      <span className="current-price">₹ {alt.price}</span>
                      <span className="original-price">₹{alt.originalPrice}</span>
                    </div>
                    <span className="save-pill">Save {alt.savePercent}</span>
                  </div>
                </div>
              ))}
            </div>

            <div className="modal-footer">
              <Shield size={16} color="#3b82f6" />
              <p>All alternatives verified for same active ingredient & dosage</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
