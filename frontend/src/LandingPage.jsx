// src/App.jsx
import './index.css';
import './App.css';

import { useNavigate } from 'react-router-dom';
import Header from './components/Header';
import AuthBox from './components/auth/Authbox';
import FeatureCard from './components/FeatureCard/FeatureCard';

import Threads from './bits/Threads';
import ScrollFloat from './bits/Scroll';
import Masonry from './components/Masonry';
import DecryptedText from './components/DecryptedText';
import CardSwap, { Card } from './bits/CardSwap';
import ScrollReveal from './bits/ScrollReveal';

import image1 from './assets/image1.jpeg';
import image2 from './assets/image2.jpeg';
import image3 from './assets/image3.jpeg';
import image4 from './assets/image4.jpeg';
import image5 from './assets/image5.jpeg';
import image6 from './assets/image6.jpeg';
import image7 from './assets/image7.jpeg';
import image8 from './assets/image8.jpeg';
import image9 from './assets/image9.jpeg';
import image10 from './assets/image10.jpeg';

function LandingPage() {
  const navigate = useNavigate();
  const items = [
    { id: '1', img: image1, height: 400 },
    { id: '2', img: image2, height: 250 },
    { id: '3', img: image3, height: 600 },
    { id: '4', img: image4, height: 380 },
    { id: '5', img: image5, height: 420 },
    { id: '6', img: image6, height: 320 },
    { id: '7', img: image7, height: 480 },
    { id: '8', img: image8, height: 300 },
    { id: '9', img: image9, height: 440 },
    { id: '10', img: image10, height: 360 },
  ];

  return (
    <div className="app-root">

      {/* Background */}
      <Threads color={[0.7, 0.7, 0.75]} amplitude={0.6} distance={0.3} />

      {/* Foreground content */}
      <div className="app-content hero-page">
        <Header
          onAuthClick={() => navigate('/dashboard')}
        />

        {/* Hero */}
        <main className="hero-section">
          <div className="container hero-layout">
            <div className="hero-left">
              <div style={{ marginBottom: '0.9rem' }}>
                <span
                  className="heading-xl"
                  style={{
                    letterSpacing: '0.18em',
                    textTransform: 'uppercase',
                  }}
                >
                  JAN-AIKYA
                </span>
              </div>

              <p className="text-lg" style={{ marginBottom: '0.5rem' }}>
                Affordable Medicine Intelligence and Access Platform.
              </p>
              <p className="text-muted">
                Enter or scan prescriptions, discover safe generics, compare prices,
                and find nearby pharmacies—all in one place.
              </p>
            </div>

            <div id="auth-box">
              <AuthBox />
            </div>
          </div>
        </main>

        {/* Features */}
        <section className="features-container">
          <ScrollFloat
            containerClassName="features-grid"
            animationDuration={1.2}
            ease="power3.out"
            scrollStart="top 85%"
            scrollEnd="bottom 35%"
            stagger={0.12}
          >
            <FeatureCard
              className="scroll-item"
              icon="💊"
              title="Generic Discovery"
              description="Effortlessly discover safe, affordable generic medicines with the exact same active ingredients."
            />
            <FeatureCard
              className="scroll-item"
              icon="📸"
              title="Smart Scanner"
              description="Upload or scan your handwritten prescriptions. We decode what you need instantly."
            />
            <FeatureCard
              className="scroll-item"
              icon="⚖️"
              title="Compare Prices"
              description="Get total transparency. Check alternative brands and compare prices at a glance."
            />
            <FeatureCard
              className="scroll-item"
              icon="📍"
              title="Locate Pharmacy"
              description="Find nearby stockists and reliable pharmacies in real-time, right around the corner."
            />
          </ScrollFloat>
        </section>

        {/* Masonry section */}
        <section className="masonry-section">
          <Masonry
            items={items}
            ease="power2.out"
            duration={1.4}
            stagger={0.05}
            animateFrom="bottom"
            scaleOnHover
            hoverScale={0.97}
            blurToFocus
            colorShiftOnHover
          />
        </section>

        {/* About section – appears after you scroll past Masonry */}
        <section className="about-section">
          <div className="container" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', paddingBottom: '2rem' }}>
            <DecryptedText
              text="About JAN-AIKYA"
              animateOn="view"
              revealDirection="center"
              sequential
              speed={70}
              maxIterations={5}
              className="about-heading"
              parentClassName="about-heading-wrapper"
              encryptedClassName="about-heading-encrypted"
            />

            <p
              className="text-lg"
              style={{ marginTop: '1.5rem', maxWidth: '48rem' }}
            >
              JAN-AIKYA is an AI-powered platform that digitizes and organizes your complete medical history from uploaded prescriptions and reports — instantly and automatically.<br /><br />
              It identifies cheaper, safety-verified generic alternatives to branded medicines and enables seamless, secure record sharing with doctors via a time-expiring QR code or link.
            </p>
          </div>
        </section>

        {/* Card Swap Interactive Section */}
        <section className="card-swap-section">
          <div className="container" style={{ display: 'flex', flexDirection: 'row', alignItems: 'center', minHeight: '800px', paddingTop: '4rem', paddingBottom: '6rem', gap: '4rem' }}>
            
            <div style={{ flex: 1 }}>
              <h2 className="heading-xl" style={{ color: '#e2e8f0', fontSize: '4rem', lineHeight: 1.15, textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                <ScrollReveal
                  baseOpacity={0.15}
                  enableBlur
                  baseRotation={1.5}
                  blurStrength={6}
                  wordAnimationEnd="top 40%"
                  rotationEnd="top 40%"
                >
                  {`WHO'S BEHIND\nJAN-AIKYA?`}
                </ScrollReveal>
              </h2>
            </div>

            <div style={{ flex: 1, display: 'flex', justifyContent: 'center' }}>
              <CardSwap pauseOnHover={true} width={380} height={500}>
                <Card className="demo-card-placeholder" style={{ background: '#0a192f', border: '1px solid rgba(56, 189, 248, 0.15)', borderRadius: '24px', overflow: 'hidden', display: 'flex', flexDirection: 'column', height: '100%', color: '#f8fafc', boxShadow: '0 15px 35px -12px rgba(0, 0, 0, 0.3)' }}>
                  <div style={{ width: '100%', height: '55%', position: 'relative' }}>
                    <img src="/src/assets/admin1.jpeg" alt="Eagar Nandi" style={{ objectFit: 'cover', width: '100%', height: '100%', objectPosition: 'center 20%' }} />
                    <div style={{ position: 'absolute', bottom: 0, left: 0, width: '100%', height: '50%', background: 'linear-gradient(to top, #0a192f, transparent)' }}></div>
                  </div>
                  <div style={{ padding: '1.5rem 2rem', flex: 1, display: 'flex', flexDirection: 'column' }}>
                    <h3 style={{ fontSize: '1.8rem', color: '#38bdf8', fontWeight: 600, margin: '0 0 0.25rem 0' }}>Eagar Nandi</h3>
                    <div style={{ color: '#94a3b8', fontSize: '1.05rem', fontWeight: 500, marginBottom: '0.2rem' }}>FrontEnd and UI/UX</div>
                    <div style={{ color: '#64748b', fontSize: '0.9rem', marginBottom: '1.5rem' }}>Techno India University</div>
                    <p style={{ color: '#f1f5f9', fontSize: '1.1rem', fontStyle: 'italic', marginTop: 'auto', borderLeft: '3px solid #38bdf8', paddingLeft: '1rem' }}>"Nobody cares until its on GITHUB"</p>
                  </div>
                </Card>

                <Card className="demo-card-placeholder" style={{ background: '#0a192f', border: '1px solid rgba(129, 140, 248, 0.15)', borderRadius: '24px', overflow: 'hidden', display: 'flex', flexDirection: 'column', height: '100%', color: '#f8fafc', boxShadow: '0 15px 35px -12px rgba(0, 0, 0, 0.3)' }}>
                  <div style={{ width: '100%', height: '55%', position: 'relative' }}>
                    <img src="/src/assets/admin2.jpeg" alt="Sarthack Das" style={{ objectFit: 'cover', width: '100%', height: '100%', objectPosition: 'center 20%' }} />
                    <div style={{ position: 'absolute', bottom: 0, left: 0, width: '100%', height: '50%', background: 'linear-gradient(to top, #0a192f, transparent)' }}></div>
                  </div>
                  <div style={{ padding: '1.5rem 2rem', flex: 1, display: 'flex', flexDirection: 'column' }}>
                    <h3 style={{ fontSize: '1.8rem', color: '#818cf8', fontWeight: 600, margin: '0 0 0.25rem 0' }}>Sarthack Das</h3>
                    <div style={{ color: '#94a3b8', fontSize: '1.05rem', fontWeight: 500, marginBottom: '0.2rem' }}>Prompt Engineer</div>
                    <div style={{ color: '#64748b', fontSize: '0.9rem', marginBottom: '1.5rem' }}>Techno India University</div>
                    <p style={{ color: '#f1f5f9', fontSize: '1.1rem', fontStyle: 'italic', marginTop: 'auto', borderLeft: '3px solid #818cf8', paddingLeft: '1rem' }}>"Trust the process"</p>
                  </div>
                </Card>

                <Card className="demo-card-placeholder" style={{ background: '#0a192f', border: '1px solid rgba(192, 132, 252, 0.15)', borderRadius: '24px', overflow: 'hidden', display: 'flex', flexDirection: 'column', height: '100%', color: '#f8fafc', boxShadow: '0 15px 35px -12px rgba(0, 0, 0, 0.3)' }}>
                  <div style={{ width: '100%', height: '55%', position: 'relative' }}>
                    <img src="/src/assets/admin3.jpeg" alt="Bineet Bairagi" style={{ objectFit: 'cover', width: '100%', height: '100%', objectPosition: 'center 20%' }} />
                    <div style={{ position: 'absolute', bottom: 0, left: 0, width: '100%', height: '50%', background: 'linear-gradient(to top, #0a192f, transparent)' }}></div>
                  </div>
                  <div style={{ padding: '1.5rem 2rem', flex: 1, display: 'flex', flexDirection: 'column' }}>
                    <h3 style={{ fontSize: '1.8rem', color: '#c084fc', fontWeight: 600, margin: '0 0 0.25rem 0' }}>Bineet Bairagi</h3>
                    <div style={{ color: '#94a3b8', fontSize: '1.05rem', fontWeight: 500, marginBottom: '0.2rem' }}>Leader and Job Planner</div>
                    <div style={{ color: '#64748b', fontSize: '0.9rem', marginBottom: '1.5rem' }}>Techno India University</div>
                    <p style={{ color: '#f1f5f9', fontSize: '1.1rem', fontStyle: 'italic', marginTop: 'auto', borderLeft: '3px solid #c084fc', paddingLeft: '1rem' }}>"Fear is the little-death that brings total obliteration"</p>
                  </div>
                </Card>

                <Card className="demo-card-placeholder" style={{ background: '#0a192f', border: '1px solid rgba(244, 114, 182, 0.15)', borderRadius: '24px', overflow: 'hidden', display: 'flex', flexDirection: 'column', height: '100%', color: '#f8fafc', boxShadow: '0 15px 35px -12px rgba(0, 0, 0, 0.3)' }}>
                  <div style={{ width: '100%', height: '55%', position: 'relative' }}>
                    <img src="/src/assets/admin4.jpeg" alt="Asmit Goswami" style={{ objectFit: 'cover', width: '100%', height: '100%', objectPosition: 'center 20%' }} />
                    <div style={{ position: 'absolute', bottom: 0, left: 0, width: '100%', height: '50%', background: 'linear-gradient(to top, #0a192f, transparent)' }}></div>
                  </div>
                  <div style={{ padding: '1.5rem 2rem', flex: 1, display: 'flex', flexDirection: 'column' }}>
                    <h3 style={{ fontSize: '1.8rem', color: '#f472b6', fontWeight: 600, margin: '0 0 0.25rem 0' }}>Asmit Goswami</h3>
                    <div style={{ color: '#94a3b8', fontSize: '1.05rem', fontWeight: 500, marginBottom: '0.2rem' }}>Backend and ML Engineer</div>
                    <div style={{ color: '#64748b', fontSize: '0.9rem', marginBottom: '1.5rem' }}>Techno India University</div>
                    <p style={{ color: '#f1f5f9', fontSize: '1.1rem', fontStyle: 'italic', marginTop: 'auto', borderLeft: '3px solid #f472b6', paddingLeft: '1rem' }}>"Give up on your dreams and Die"</p>
                  </div>
                </Card>

                <Card className="demo-card-placeholder" style={{ background: '#0a192f', border: '1px solid rgba(167, 243, 208, 0.15)', borderRadius: '24px', overflow: 'hidden', display: 'flex', flexDirection: 'column', height: '100%', color: '#f8fafc', boxShadow: '0 15px 35px -12px rgba(0, 0, 0, 0.3)' }}>
                  <div style={{ width: '100%', height: '55%', position: 'relative' }}>
                    <img src="/src/assets/admin5.jpeg" alt="Urshashi Majumder" style={{ objectFit: 'cover', width: '100%', height: '100%', objectPosition: 'center 20%' }} />
                    <div style={{ position: 'absolute', bottom: 0, left: 0, width: '100%', height: '50%', background: 'linear-gradient(to top, #0a192f, transparent)' }}></div>
                  </div>
                  <div style={{ padding: '1.5rem 2rem', flex: 1, display: 'flex', flexDirection: 'column' }}>
                    <h3 style={{ fontSize: '1.8rem', color: '#34d399', fontWeight: 600, margin: '0 0 0.25rem 0' }}>Urshashi Majumder</h3>
                    <div style={{ color: '#94a3b8', fontSize: '1.05rem', fontWeight: 500, marginBottom: '0.2rem' }}>Research/Development</div>
                    <div style={{ color: '#64748b', fontSize: '0.9rem', marginBottom: '1.5rem' }}>Techno India University</div>
                    <p style={{ color: '#f1f5f9', fontSize: '1.1rem', fontStyle: 'italic', marginTop: 'auto', borderLeft: '3px solid #34d399', paddingLeft: '1rem' }}>"Slow and Steady"</p>
                  </div>
                </Card>
              </CardSwap>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}

export default LandingPage;