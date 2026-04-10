"""
Records routes — upload medical documents, retrieve patient records.

POST /api/records/upload  → Upload document + optional voice note → runs Agent 1
GET  /api/records          → List all records for the authenticated patient
"""

import uuid
import json
import logging
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from typing import Optional

from core.auth import get_current_user
from core.supabase_client import get_service_client
from agents.agent_1_intake import extract_from_image, extract_from_pdf_bytes, merge_with_transcription
from services.whisper_service import transcribe_audio

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/records", tags=["Medical Records"])

# Allowed MIME types
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
ALLOWED_PDF_TYPES = {"application/pdf"}
ALLOWED_AUDIO_TYPES = {
    "audio/wav", "audio/mpeg", "audio/mp3", "audio/mp4",
    "audio/m4a", "audio/webm", "audio/ogg", "audio/x-wav",
}


@router.post("/upload")
async def upload_record(
    file: UploadFile = File(..., description="Prescription/report image or PDF"),
    file_type: str = Form("prescription", description="prescription, lab_report, or imaging"),
    voice_note: Optional[UploadFile] = File(None, description="Optional voice note audio"),
    user_id: str = Depends(get_current_user),
):
    """
    Upload a medical document (image/PDF) with an optional voice note.
    Runs Agent 1 for extraction and merges voice transcription if provided.
    Saves everything to Supabase (Storage + DB).
    """
    client = get_service_client()

    # ── Validate file type ──
    content_type = file.content_type or ""
    if content_type not in ALLOWED_IMAGE_TYPES and content_type not in ALLOWED_PDF_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {content_type}. Upload an image or PDF.",
        )

    if file_type not in ("prescription", "lab_report", "imaging"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="file_type must be 'prescription', 'lab_report', or 'imaging'.",
        )

    # ── Read file bytes ──
    file_bytes = await file.read()
    file_ext = file.filename.split(".")[-1] if file.filename else "bin"
    storage_filename = f"{user_id}/{uuid.uuid4()}.{file_ext}"

    # ── Upload document to Supabase Storage ──
    try:
        client.storage.from_("prescriptions").upload(
            path=storage_filename,
            file=file_bytes,
            file_options={"content-type": content_type},
        )
        file_url = client.storage.from_("prescriptions").get_public_url(storage_filename)
    except Exception as e:
        logger.error(f"Storage upload failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file: {str(e)}",
        )

    # ── Process voice note (if provided) ──
    voice_note_url = None
    transcription = None

    if voice_note is not None:
        voice_content_type = voice_note.content_type or ""
        if voice_content_type not in ALLOWED_AUDIO_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported audio type: {voice_content_type}.",
            )

        voice_bytes = await voice_note.read()
        voice_ext = voice_note.filename.split(".")[-1] if voice_note.filename else "wav"
        voice_storage_path = f"{user_id}/{uuid.uuid4()}.{voice_ext}"

        # Upload voice note
        try:
            client.storage.from_("voice-notes").upload(
                path=voice_storage_path,
                file=voice_bytes,
                file_options={"content-type": voice_content_type},
            )
            voice_note_url = client.storage.from_("voice-notes").get_public_url(voice_storage_path)
        except Exception as e:
            logger.warning(f"Voice note upload failed: {e}")

        # Transcribe with Whisper
        try:
            whisper_result = await transcribe_audio(voice_bytes, voice_note.filename or "audio.wav")
            transcription = whisper_result.get("text", "")
        except Exception as e:
            logger.warning(f"Whisper transcription failed: {e}")

    # ── Run Agent 1: Document Intake ──
    try:
        if content_type in ALLOWED_PDF_TYPES:
            extracted_data = await extract_from_pdf_bytes(file_bytes)
        else:
            extracted_data = await extract_from_image(file_bytes, mime_type=content_type)

        # Merge with voice transcription if available
        if transcription:
            extracted_data = await merge_with_transcription(extracted_data, transcription)

    except Exception as e:
        logger.error(f"Agent 1 extraction failed: {e}")
        extracted_data = {
            "medicines": [],
            "diagnosis": None,
            "doctor_name": None,
            "hospital": None,
            "date": None,
            "notes": f"Extraction failed: {str(e)}",
        }

    # ── Save extracted medicine list as JSON to storage ──
    if extracted_data.get("medicines"):
        try:
            medicine_json = json.dumps(extracted_data["medicines"], indent=2).encode("utf-8")
            medicine_path = f"{user_id}/medicines_{uuid.uuid4()}.json"
            client.storage.from_("generated-files").upload(
                path=medicine_path,
                file=medicine_json,
                file_options={"content-type": "application/json"},
            )
        except Exception as e:
            logger.warning(f"Failed to save medicine list JSON: {e}")

    # ── Save record to database ──
    record_data = {
        "patient_id": user_id,
        "file_url": file_url,
        "file_type": file_type,
        "original_filename": file.filename or "unknown",
        "extracted_data": extracted_data,
        "voice_note_url": voice_note_url,
        "transcription": transcription,
    }

    try:
        response = (
            client.table("medical_records")
            .insert(record_data)
            .execute()
        )
        record = response.data[0] if response.data else record_data
    except Exception as e:
        logger.error(f"Database insert failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save record: {str(e)}",
        )

    return {
        "message": "Record uploaded and processed successfully",
        "record": record,
        "extraction": extracted_data,
    }


@router.get("")
async def get_records(user_id: str = Depends(get_current_user)):
    """Get all medical records for the authenticated patient."""
    client = get_service_client()

    response = (
        client.table("medical_records")
        .select("*")
        .eq("patient_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )

    return {
        "records": response.data or [],
        "count": len(response.data or []),
    }
