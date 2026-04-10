"""
Voice routes — Whisper transcription and gTTS synthesis.

POST /api/voice/transcribe  → Upload audio → Whisper STT
POST /api/voice/speak       → Text → gTTS audio (with Supabase upload)
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import Response

from models.schemas import TTSRequest, TTSResponse, TranscriptionResponse
from core.auth import get_current_user
from services.whisper_service import transcribe_audio
from services.tts_service import synthesize_and_upload, synthesize_to_bytes

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/voice", tags=["Voice"])

ALLOWED_AUDIO_TYPES = {
    "audio/wav", "audio/mpeg", "audio/mp3", "audio/mp4",
    "audio/m4a", "audio/webm", "audio/ogg", "audio/x-wav",
    "audio/x-m4a", "audio/flac",
}


@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_voice(
    audio: UploadFile = File(..., description="Audio file to transcribe"),
    user_id: str = Depends(get_current_user),
):
    """
    Transcribe an audio file using local Whisper model.
    Supports multilingual input including Indian languages.
    """
    content_type = audio.content_type or ""

    # Allow common audio types
    if content_type not in ALLOWED_AUDIO_TYPES:
        # Be lenient — try anyway if extension looks right
        ext = (audio.filename or "").rsplit(".", 1)[-1].lower()
        if ext not in ("wav", "mp3", "m4a", "webm", "ogg", "flac", "mp4"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported audio format: {content_type}",
            )

    audio_bytes = await audio.read()

    if not audio_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty audio file.",
        )

    try:
        result = await transcribe_audio(audio_bytes, audio.filename or "audio.wav")

        return TranscriptionResponse(
            text=result["text"],
            language=result.get("language"),
        )

    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Transcription failed: {str(e)}",
        )


@router.post("/speak", response_model=TTSResponse)
async def text_to_speech(
    req: TTSRequest,
    user_id: str = Depends(get_current_user),
):
    """
    Convert text to speech using gTTS.
    Uploads the audio to Supabase Storage and returns the URL.

    Supported languages: en, hi, ta, te, bn, mr, gu, kn, ml
    """
    if not req.text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text cannot be empty.",
        )

    try:
        audio_url = await synthesize_and_upload(
            text=req.text,
            language=req.language,
            user_id=user_id,
        )

        return TTSResponse(audio_url=audio_url)

    except Exception as e:
        logger.error(f"TTS failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Text-to-speech failed: {str(e)}",
        )


@router.post("/speak/stream")
async def text_to_speech_stream(
    req: TTSRequest,
    user_id: str = Depends(get_current_user),
):
    """
    Convert text to speech and return the audio directly as an MP3 response.
    Does NOT upload to storage — useful for immediate playback.
    """
    if not req.text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text cannot be empty.",
        )

    try:
        audio_bytes = await synthesize_to_bytes(
            text=req.text,
            language=req.language,
        )

        return Response(
            content=audio_bytes,
            media_type="audio/mpeg",
            headers={"Content-Disposition": "inline; filename=speech.mp3"},
        )

    except Exception as e:
        logger.error(f"TTS stream failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Text-to-speech failed: {str(e)}",
        )
