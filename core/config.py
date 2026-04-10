"""
Application configuration — loads all settings from .env file.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """All environment variables used by the application."""

    # ── Supabase ──
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str
    SUPABASE_JWT_SECRET: str = ""  # Optional: used for local JWT verification

    # ── Gemini ──
    GEMINI_API_KEY: str

    # ── OpenRouter ──
    OPENROUTER_API_KEY: str

    # ── Whisper ──
    WHISPER_MODEL: str = "base"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Cached settings singleton — reads .env once."""
    return Settings()
