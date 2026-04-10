"""
Text-to-Speech Service — uses gTTS (Google Translate TTS).
Free, no API key required. Supports Indian languages.

Supported language codes:
  en (English), hi (Hindi), ta (Tamil), te (Telugu),
  bn (Bengali), mr (Marathi), gu (Gujarati), kn (Kannada), ml (Malayalam)
"""

import tempfile
import os
import uuid
import logging
from gtts import gTTS

from core.supabase_client import get_service_client

logger = logging.getLogger(__name__)

# Supported languages for TTS
SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu",
    "bn": "Bengali",
    "mr": "Marathi",
    "gu": "Gujarati",
    "kn": "Kannada",
    "ml": "Malayalam",
}


async def synthesize_and_upload(
    text: str,
    language: str = "en",
    user_id: str | None = None,
) -> str:
    """
    Convert text to speech using gTTS and upload to Supabase Storage.

    Args:
        text: The text to synthesize.
        language: Language code (default "en").
        user_id: Optional user ID for organizing files.

    Returns:
        Public URL of the uploaded audio file.
    """
    if language not in SUPPORTED_LANGUAGES:
        logger.warning(f"Unsupported language '{language}', falling back to English")
        language = "en"

    # Generate audio
    tts = gTTS(text=text, lang=language, slow=False)

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tts.save(tmp.name)
        tmp_path = tmp.name

    try:
        # Read the generated audio file
        with open(tmp_path, "rb") as f:
            audio_bytes = f.read()

        # Upload to Supabase Storage
        file_id = str(uuid.uuid4())
        folder = user_id or "system"
        storage_path = f"{folder}/tts_{file_id}.mp3"

        client = get_service_client()
        client.storage.from_("generated-files").upload(
            path=storage_path,
            file=audio_bytes,
            file_options={"content-type": "audio/mpeg"},
        )

        # Get public URL
        url_response = client.storage.from_("generated-files").get_public_url(storage_path)

        logger.info(f"TTS audio uploaded: {storage_path}")
        return url_response

    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


async def synthesize_to_bytes(text: str, language: str = "en") -> bytes:
    """
    Convert text to speech and return raw MP3 bytes (no upload).

    Useful for streaming or direct response.
    """
    if language not in SUPPORTED_LANGUAGES:
        language = "en"

    tts = gTTS(text=text, lang=language, slow=False)

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tts.save(tmp.name)
        tmp_path = tmp.name

    try:
        with open(tmp_path, "rb") as f:
            return f.read()
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
