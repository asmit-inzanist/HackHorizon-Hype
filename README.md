# 🏥 JAN-AIKYA
### Unified Personal Health Record & Affordable Medicine Intelligence Platform

> *"Jan" (जन) = People | "Aikya" (ऐक्य) = Unity — Uniting people with their health data and affordable medicine.*

Built for **HackHorizon 2K26** — combining Problem Statements A (Unified Health Records) and C (Affordable Medicine Intelligence).

---

## 🌟 What is JAN-AIKYA?

JAN-AIKYA is a full-stack AI-powered health platform that solves two critical healthcare challenges simultaneously:

1. **Centralized Health Records** — Patients can securely upload, store, and share their complete medical history (prescriptions, lab reports, imaging) in one place, with instant AI-generated summaries for doctors.

2. **Affordable Medicine Intelligence** — When a prescription is uploaded, our AI agents automatically find cheaper generic alternatives with full formulation compatibility, CDSCO regulatory approval checks, dosage verification, and long-term cost savings projections.

---

## 🤖 The 4 AI Agents

| Agent | Model | Role |
|---|---|---|
| **Agent 1 — Document Intake** | Gemini 1.5 Flash (Vision) | Reads prescriptions/PDFs, extracts structured medicine + diagnosis data, merges voice notes |
| **Agent 2 — Medicine Analyzer** | Llama 3.3 70B (OpenRouter) | Finds cheaper generic alternatives, checks formulation + dosage compatibility, calculates monthly/yearly savings |
| **Agent 3 — Patient Summarizer** | Gemini 1.5 Flash | Generates doctor-facing summaries, cross-checks allergies, triggers audio TTS allergy alerts |
| **Agent 4 — Web Researcher** | Gemini 1.5 Flash + Google Search | Searches real-time Indian market prices, CDSCO approval status, formulation types, therapeutic categories |

---

## 🚀 Features

- 📄 **AI Document Extraction** — Upload any prescription image or PDF, Agent 1 reads it instantly
- 🎤 **Voice Notes** — Record a voice note alongside your prescription; Whisper AI transcribes it in any Indian language
- 💊 **Generic Medicine Finder** — Compare brand vs generic prices with ✅ ⚠️ ❌ formulation compatibility flags
- 📊 **Long-term Cost Projections** — Monthly, yearly, and 5-year savings calculations
- 🏷️ **Therapeutic Category** — Every medicine categorized (antibiotic, NSAID, antihypertensive, etc.)
- 🔔 **Allergy Alert System** — Audio TTS warning triggered if prescription conflicts with patient's allergies
- 🗺️ **Pharmacy Finder** — Find nearby pharmacies using OpenStreetMap with one-click Google Maps walking directions
- 🔗 **Secure Sharing** — 24-hour expiring token links for sharing complete medical history with doctors
- 📬 **File Sharing** — Send specific records directly to another user by email
- 🗣️ **Multilingual TTS** — Text-to-speech in English, Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam

---

## 🧱 Tech Stack

### Backend
| Layer | Technology |
|---|---|
| Framework | FastAPI + Uvicorn |
| Database | Supabase (PostgreSQL + Row Level Security) |
| Storage | Supabase Storage (prescriptions, voice notes, generated files) |
| Auth | Supabase JWT |
| AI — Vision/Text | Google Gemini 1.5 Flash (`google-genai`) |
| AI — Analysis | Llama 3.3 70B via OpenRouter (free tier) |
| AI — Search | Gemini 1.5 Flash + Google Search Grounding |
| STT | OpenAI Whisper `base` (local, multilingual) |
| TTS | gTTS (Google Translate TTS, free, no API key) |
| Pharmacy Search | Overpass API (OpenStreetMap, free) |
| HTTP Client | httpx (async) |
| Validation | Pydantic v2 |

---

## 📁 Project Structure

```
JAN-AIKYA/
├── README.md
├── LICENSE
├── .gitignore
│
└── backend/
    ├── main.py                     # FastAPI app entry point
    ├── requirements.txt            # Python dependencies
    ├── .env.example                # Environment variables template
    ├── implementation_plan.md      # Full technical design doc
    │
    ├── core/
    │   ├── config.py               # Pydantic Settings (.env loader)
    │   ├── auth.py                 # Supabase JWT auth dependency
    │   └── supabase_client.py      # Supabase client singletons
    │
    ├── models/
    │   └── schemas.py              # All Pydantic request/response models
    │
    ├── agents/
    │   ├── agent_1_intake.py       # Gemini Flash Vision — document extraction
    │   ├── agent_2_analyzer.py     # Llama 3.3 — medicine analysis + cost projections
    │   ├── agent_3_summarizer.py   # Gemini Flash — patient summary + allergy alerts
    │   └── agent_4_research.py     # Gemini + Search Grounding — real-time price research
    │
    ├── services/
    │   ├── whisper_service.py      # Local Whisper multilingual STT
    │   ├── tts_service.py          # gTTS multilingual TTS + Supabase upload
    │   └── overpass_service.py     # Pharmacy discovery via OpenStreetMap
    │
    ├── api/routes/
    │   ├── auth.py                 # POST /api/auth/signup, /api/auth/login
    │   ├── profile.py              # GET/PUT /api/profile
    │   ├── records.py              # POST /api/records/upload, GET /api/records
    │   ├── medicines.py            # GET /api/medicines/{record_id}
    │   ├── share.py                # POST /api/share, GET /api/share/{token}
    │   ├── summary.py              # GET /api/patient/summary
    │   ├── pharmacies.py           # GET /api/pharmacies/nearby
    │   └── voice.py                # POST /api/voice/transcribe, /api/voice/speak
    │
    └── scripts/
        └── setup_database.sql      # Full Supabase migration (6 tables + RLS + buckets)
```

---

## ⚡ Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/asmit-inzanist/HackHorizon-Hype.git
cd HackHorizon-Hype/backend
```

### 2. Create virtual environment
```bash
python -m venv venv
.\venv\Scripts\activate        # Windows
# or
source venv/bin/activate       # Linux/Mac
```

### 3. Install dependencies
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your actual keys
```

Required keys:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
SUPABASE_JWT_SECRET=your-jwt-secret
GEMINI_API_KEY=your-gemini-api-key
OPENROUTER_API_KEY=your-openrouter-api-key
WHISPER_MODEL=base
```

### 5. Set up the database
Go to your **Supabase Dashboard → SQL Editor**, paste the contents of `scripts/setup_database.sql` and run it. This creates all 6 tables, RLS policies, triggers, and storage buckets.

### 6. Run the server
```bash
uvicorn main:app --reload --port 8000
```

Visit **http://localhost:8000/docs** for the interactive Swagger API documentation.

---

## 🌐 API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/api/auth/signup` | ❌ | Register a new user |
| `POST` | `/api/auth/login` | ❌ | Login — returns JWT |
| `GET` | `/api/profile` | ✅ | Get health profile |
| `PUT` | `/api/profile` | ✅ | Update health profile (allergies, conditions) |
| `POST` | `/api/records/upload` | ✅ | Upload prescription/report + optional voice note → Agent 1 |
| `GET` | `/api/records` | ✅ | List all records |
| `GET` | `/api/medicines/{record_id}` | ✅ | Get generic alternatives + cost analysis → Agent 2 + 4 |
| `GET` | `/api/patient/summary` | ✅ | AI patient summary + allergy check → Agent 3 |
| `GET` | `/api/pharmacies/nearby` | ✅ | Find nearby pharmacies (lat, lon, radius_km) |
| `POST` | `/api/share` | ✅ | Generate 24h sharing link |
| `GET` | `/api/share/{token}` | ❌ | Public doctor view via token |
| `POST` | `/api/share/file` | ✅ | Share record with user by email |
| `GET` | `/api/share/inbox` | ✅ | View received files |
| `POST` | `/api/voice/transcribe` | ✅ | Audio → Whisper transcription |
| `POST` | `/api/voice/speak` | ✅ | Text → gTTS audio URL |

---

## 🗃️ Database Schema

6 tables with full Row Level Security (RLS):
- **`profiles`** — Patient health profiles (allergies, chronic conditions, blood group)
- **`medical_records`** — Uploaded documents with AI-extracted structured data
- **`medicine_analyses`** — Agent 2+4 generic alternatives + cost projections
- **`patient_summaries`** — Agent 3 AI summaries + allergy warnings + audio URL
- **`share_tokens`** — 24-hour expiring doctor share links
- **`shared_files`** — User-to-user direct file sharing

---

## 🏆 HackHorizon 2K26

**Problem Statements Addressed:**
- **A — Unified Personal Health Record & Secure Medical Data Sharing Platform**
- **C — Affordable Medicine Intelligence and Access Platform**

**Team:** [Your Team Name]

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
