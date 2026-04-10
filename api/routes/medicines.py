"""
Medicines routes — trigger Agent 2 + Agent 4 pipeline for medicine analysis.

GET /api/medicines/{record_id}  → Get/trigger medicine alternatives for a record
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status

from core.auth import get_current_user
from core.supabase_client import get_service_client
from agents.agent_2_analyzer import analyze_medicines

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/medicines", tags=["Medicine Analysis"])


@router.get("/{record_id}")
async def get_medicine_alternatives(
    record_id: str,
    user_id: str = Depends(get_current_user),
):
    """
    Get medicine alternatives and price comparisons for a given medical record.
    If an analysis already exists, return it. Otherwise run the Agent 2+4 pipeline.
    """
    client = get_service_client()

    # ── Check if analysis already exists ──
    existing = (
        client.table("medicine_analyses")
        .select("*")
        .eq("record_id", record_id)
        .eq("patient_id", user_id)
        .execute()
    )

    if existing.data:
        return {
            "message": "Existing analysis found",
            "analysis": existing.data[0],
        }

    # ── Fetch the record to get extracted data ──
    record_response = (
        client.table("medical_records")
        .select("*")
        .eq("id", record_id)
        .eq("patient_id", user_id)
        .single()
        .execute()
    )

    if not record_response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical record not found.",
        )

    record = record_response.data
    extracted_data = record.get("extracted_data", {})

    # ── Run Agent 2 + Agent 4 pipeline ──
    logger.info(f"Running medicine analysis for record {record_id}")

    try:
        analysis_result = await analyze_medicines(extracted_data)
    except Exception as e:
        logger.error(f"Medicine analysis failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Medicine analysis failed: {str(e)}",
        )

    # ── Save analysis to database ──
    analysis_data = {
        "record_id": record_id,
        "patient_id": user_id,
        "medicines": analysis_result.get("medicines", []),
        "total_savings": analysis_result.get("total_savings", 0.0),
    }

    try:
        save_response = (
            client.table("medicine_analyses")
            .insert(analysis_data)
            .execute()
        )
        saved = save_response.data[0] if save_response.data else analysis_data
    except Exception as e:
        logger.error(f"Failed to save analysis: {e}")
        saved = analysis_data

    return {
        "message": "Medicine analysis complete",
        "analysis": saved,
        "summary": analysis_result.get("summary", ""),
    }
