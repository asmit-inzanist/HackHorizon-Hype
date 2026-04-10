"""
Whisper STT Service — Local speech-to-text using OpenAI Whisper (base model).
Supports multilingual transcription including Indian languages.
"""

import whisper
import tempfile
import os
import logging

logger = logging.getLogger(__name__)

# Global model instance — loaded once at startup
_model: whisper.Whisper | None = None


def load_model(model_name: str = "base") -> None:
    """Pre-load the Whisper model into memory."""
    global _model
    if _model is None:
        logger.info(f"Loading Whisper model: {model_name}")
        _model = whisper.load_model(model_name)
        logger.info("Whisper model loaded successfully")


def get_model() -> whisper.Whisper:
    """Get the loaded Whisper model, loading it if necessary."""
    global _model
    if _model is None:
        load_model()
    return _model


async def transcribe_audio(audio_bytes: bytes, filename: str = "audio.wav") -> dict:
    """
    Transcribe audio bytes using Whisper.

    Args:
        audio_bytes: Raw audio file bytes (wav, mp3, m4a, etc.)
        filename: Original filename for extension detection

    Returns:
        dict with keys: text, language
    """
    model = get_model()

    # Write audio to a temporary file (Whisper requires a file path)
    suffix = os.path.splitext(filename)[1] or ".wav"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        logger.info(f"Transcribing audio file: {filename}")

        # Transcribe with auto language detection
        result = model.transcribe(
            tmp_path,
            fp16=False,  # Use fp32 for CPU compatibility
        )

        detected_language = result.get("language", "unknown")
        text = result.get("text", "").strip()

        logger.info(f"Transcription complete — language: {detected_language}, length: {len(text)} chars")

        return {
            "text": text,
            "language": detected_language,
        }

    finally:
        # Clean up temp file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
