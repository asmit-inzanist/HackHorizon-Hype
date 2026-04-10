import { useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import { Menu } from 'lucide-react';
import Sidebar from './Sidebar';
import OverviewRoute from './OverviewRoute';
import UploadRoute from './UploadRoute';
import MedicinesRoute from './MedicinesRoute';
import ShareRoute from './ShareRoute';
import ProfileRoute from './ProfileRoute';
import ClinicsRoute from './ClinicsRoute';
import SoftAurora from '../../bits/SoftArora';
import './DashboardLayout.css';

export default function DashboardLayout() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  return (
    <div className="dashboard-layout">
      
      {/* Global Dashboard Animated Background */}
      <div style={{ position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', zIndex: 0, pointerEvents: 'none' }}>
        <SoftAurora
          speed={0.6}
          scale={1.5}
          brightness={1}
          color1="#f7f7f7"
          color2="#e100ff"
          noiseFrequency={2.5}
          noiseAmplitude={1}
          bandHeight={0.5}
          bandSpread={1}
          octaveDecay={0.1}
          layerOffset={0}
          colorSpeed={1}
          enableMouseInteraction={true}
          mouseInfluence={0.25}
        />
      </div>

      <header className="dashboard-top-nav" style={{ position: 'sticky', zIndex: 100 }}>
        <button className="menu-toggle-btn" onClick={() => setIsSidebarOpen(true)}>
          <Menu size={24} />
        </button>
        <div className="nav-brand-text">Jan-Aikya Dashboard</div>
      </header>

      <Sidebar isOpen={isSidebarOpen} onClose={() => setIsSidebarOpen(false)} />
      
      <main className="dashboard-content" style={{ position: 'relative', zIndex: 10 }}>
        <Routes>
          <Route index element={<OverviewRoute />} />
          <Route path="upload" element={<UploadRoute />} />
          <Route path="medicines" element={<MedicinesRoute />} />
          <Route path="share" element={<ShareRoute />} />
          <Route path="profile" element={<ProfileRoute />} />
          <Route path="clinics" element={<ClinicsRoute />} />
        </Routes>
      </main>
    </div>
  );
}
