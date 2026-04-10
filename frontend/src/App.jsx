import { Routes, Route } from 'react-router-dom';
import LandingPage from './LandingPage';
import DashboardLayout from './pages/Dashboard/DashboardLayout';
import SplashCursor from './bits/SplashCursor';
import './App.css';


function App() {
  return (
    <>
      <SplashCursor SPLAT_RADIUS={0.02} SPLAT_FORCE={1000} DENSITY_DISSIPATION={12.0} VELOCITY_DISSIPATION={10.0} />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/dashboard/*" element={<DashboardLayout />} />
      </Routes>
    </>
  );
}

export default App;