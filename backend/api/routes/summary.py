"""
Summary routes — trigger Agent 3 for patient record summarization.

GET /api/patient/summary  → Generate/get AI patient summary with allergy cross-check
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status

from core.auth import get_current_user
from core.supabase_client import get_service_client
from agents.agent_3_summarizer import generate_summary

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/patient", tags=["Patient Summary"])


@router.get("/summary")
async def get_patient_summary(
    force_refresh: bool = False,
    user_id: str = Depends(get_current_user),
):
    """
    Generate or retrieve the AI patient summary.
    Includes allergy cross-checking and TTS audio for warnings.

    Query params:
        force_refresh: If true, regenerate even if a summary exists.
    """
    client = get_service_client()

    # ── Check for existing summary (unless force_refresh) ──
    if not force_refresh:
        existing = (
            client.table("patient_summaries")
            .select("*")
            .eq("patient_id", user_id)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )

        if existing.data:
            return {
                "message": "Existing summary found",
                "summary": existing.data[0],
            }

    # ── Fetch patient profile ──
    profile_response = (
        client.table("profiles")
        .select("*")
        .eq("id", user_id)
        .single()
        .execute()
    )

    if not profile_response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found. Please create your profile first.",
        )

    patient_profile = profile_response.data

    # ── Fetch all medical records ──
    records_response = (
        client.table("medical_records")
        .select("*")
        .eq("patient_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )

    medical_records = records_response.data or []

    if not medical_records:
        return {
            "message": "No medical records found. Upload records first.",
            "summary": None,
        }

    # ── Run Agent 3: Record Summarizer ──
    logger.info(f"Running Agent 3 summary for patient {user_id}")

    try:
        summary_result = await generate_summary(
            patient_profile=patient_profile,
            medical_records=medical_records,
            user_id=user_id,
        )
    except Exception as e:
        logger.error(f"Summary generation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Summary generation failed: {str(e)}",
        )

    # ── Save summary to database ──
    summary_data = {
        "patient_id": user_id,
        "summary_text": summary_result.get("summary_text", ""),
        "allergy_warnings": summary_result.get("allergy_warnings", []),
        "audio_url": summary_result.get("audio_url"),
    }

    try:
        save_response = (
            client.table("patient_summaries")
            .insert(summary_data)
            .execute()
        )
        saved = save_response.data[0] if save_response.data else summary_data
    except Exception as e:
        logger.error(f"Failed to save summary: {e}")
        saved = summary_data

    return {
        "message": "Summary generated successfully",
        "summary": saved,
        "key_observations": summary_result.get("key_observations", []),
    }
