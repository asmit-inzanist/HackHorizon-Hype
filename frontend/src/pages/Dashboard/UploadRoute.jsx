import { useState } from 'react';
import { Upload, FileText, Sparkles, Send, Mic } from 'lucide-react';
import BorderGlow from '../../bits/BorderGlow';
import './UploadRoute.css';

export default function UploadRoute() {
  const [activeTab, setActiveTab] = useState('scan');
  const [showChat, setShowChat] = useState(false);

  return (
    <div className="upload-route">
      <header className="dashboard-header">
        <h1>Upload Prescription</h1>
        <p>Upload a prescription image or enter medicines manually</p>
      </header>

      <div className="upload-tabs">
        <button 
          className={`upload-tab ${activeTab === 'scan' ? 'active' : ''}`}
          onClick={() => setActiveTab('scan')}
        >
          <FileText size={22} />
          Scan Prescription
        </button>
        <button 
          className={`upload-tab ${activeTab === 'manual' ? 'active' : ''}`}
          onClick={() => {
            setActiveTab('manual');
            setShowChat(false);
          }}
        >
           <FileText size={22} />
          Manual Entry
        </button>
      </div>

      <div className="dashboard-card upload-container">
        {activeTab === 'scan' ? (
          <>
            <div className="upload-header">
              <h3>Upload Prescription</h3>
              <p>We'll use AI to extract medicine details automatically</p>
            </div>
            
            <div className="dropzone">
              <div className="dropzone-icon">
                <Upload size={48} />
              </div>
              <h4>Drop your prescription here</h4>
              <p>or click to browse • PDF, JPG, PNG up to 10MB</p>
            </div>

            <button className="upload-btn primary-btn" onClick={() => setShowChat(true)}>
              <Sparkles size={22} />
              Upload & Extract
            </button>
          </>
        ) : (
          <div className="manual-entry">
            <h3>Manual Entry</h3>
            <p>Type in your medicines one by one.</p>
            <input type="text" placeholder="e.g. Paracetamol 500mg" className="modern-input" style={{marginTop: '1rem'}} />
            <button className="upload-btn primary-btn" style={{marginTop: '1rem'}}>
              Save Medicine
            </button>
          </div>
        )}
      </div>

      {showChat && (
        <div className="output-chat-container">
          <BorderGlow glowColor="210 100 50" borderRadius={24} backgroundColor="#030f26" className="chat-glow-card">
            <div className="chatbox-header">
              <h3>AI Extraction Results</h3>
              <p>Chat with our AI to refine boundaries or clarify details.</p>
            </div>
            
            <div className="chatbox-messages">
              <div className="chat-bubble ai-bubble">
                <Sparkles size={16} className="ai-icon-sparkle" style={{ flexShrink: 0, marginTop: '4px', color: '#38bdf8' }} />
                <div className="bubble-content">
                  I've successfully scanned your prescription! It looks like you've been prescribed <strong>Paracetamol 500mg</strong> and <strong>Amoxicillin 250mg</strong>. Let me know if you need any adjustments or alternatives.
                </div>
              </div>
            </div>

            <div className="chatbox-input-area">
              <input type="text" className="chat-input" placeholder="Type your message..." />
              <button className="icon-btn mic-btn">
                <Mic size={20} />
              </button>
              <button className="icon-btn send-btn">
                <Send size={20} />
              </button>
            </div>
          </BorderGlow>
        </div>
      )}
    </div>
  );
}
