"""
Unified Personal Health Record & Affordable Medicine Intelligence Platform
──────────────────────────────────────────────────────────────────────────
FastAPI backend with 4 AI agents for medical document processing,
medicine alternative research, patient record summarization, and
web-based price research.

Run with:  uvicorn main:app --reload --port 8000
Docs at:   http://localhost:8000/docs
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import get_settings

# ── Import all route modules ──
from api.routes import auth, profile, records, medicines, share, summary, pharmacies, voice

# ── Logging ──
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(name)-30s │ %(levelname)-7s │ %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown events.
    Pre-loads the Whisper model on startup so the first transcription is fast.
    """
    logger.info("="*60)
    logger.info("  Health Record Platform — Starting up")
    logger.info("="*60)

    # Pre-load Whisper model
    try:
        from services.whisper_service import load_model
        settings = get_settings()
        load_model(settings.WHISPER_MODEL)
        logger.info(f"Whisper model '{settings.WHISPER_MODEL}' loaded")
    except Exception as e:
        logger.warning(f"Whisper model pre-load failed (will load on first use): {e}")

    # Verify Supabase connection
    try:
        from core.supabase_client import get_service_client
        client = get_service_client()
        logger.info(f"Supabase connected: {get_settings().SUPABASE_URL}")
    except Exception as e:
        logger.error(f"Supabase connection failed: {e}")

    yield

    logger.info("Health Record Platform — Shutting down")


# ── Create FastAPI app ──
app = FastAPI(
    title="Health Record & Medicine Intelligence API",
    description=(
        "Unified Personal Health Record platform with AI-powered "
        "document extraction, medicine alternative analysis, "
        "patient summarization, and voice features."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS Middleware ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register all routers ──
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(records.router)
app.include_router(medicines.router)
app.include_router(share.router)
app.include_router(summary.router)
app.include_router(pharmacies.router)
app.include_router(voice.router)


# ── Health check ──
@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "healthy",
        "service": "Health Record & Medicine Intelligence API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}
