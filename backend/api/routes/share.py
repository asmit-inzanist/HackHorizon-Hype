"""
Share routes — token-based sharing and direct file sharing.

POST /api/share           → Generate 24h share token link
GET  /api/share/{token}   → Public: doctor views patient via token
POST /api/share/file      → Share a specific file with another user by email
GET  /api/share/inbox     → View files shared with the authenticated user
"""

import secrets
import logging
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status, Request

from models.schemas import ShareTokenResponse, ShareFileRequest
from core.auth import get_current_user
from core.supabase_client import get_service_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/share", tags=["Sharing"])

TOKEN_EXPIRY_HOURS = 24


@router.post("", response_model=ShareTokenResponse)
async def generate_share_link(
    request: Request,
    user_id: str = Depends(get_current_user),
):
    """
    Generate a secure, 24-hour expiring link for sharing the patient's
    complete medical history and AI summary with a doctor.
    """
    client = get_service_client()

    # Generate a secure random token
    token = secrets.token_urlsafe(48)
    expires_at = datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRY_HOURS)

    # Save token to database
    token_data = {
        "patient_id": user_id,
        "token": token,
        "expires_at": expires_at.isoformat(),
    }

    try:
        client.table("share_tokens").insert(token_data).execute()
    except Exception as e:
        logger.error(f"Failed to save share token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate share link.",
        )

    # Build the share URL
    base_url = str(request.base_url).rstrip("/")
    share_url = f"{base_url}/api/share/{token}"

    return ShareTokenResponse(
        token=token,
        share_url=share_url,
        expires_at=expires_at.isoformat(),
    )


@router.post("/file")
async def share_file_with_user(
    req: ShareFileRequest,
    user_id: str = Depends(get_current_user),
):
    """
    Share a specific medical record file with another user by their email.
    """
    client = get_service_client()

    # Verify the record belongs to the sender
    record_check = (
        client.table("medical_records")
        .select("id")
        .eq("id", req.record_id)
        .eq("patient_id", user_id)
        .single()
        .execute()
    )

    if not record_check.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found or you don't own this record.",
        )

    # Create the shared file entry
    share_data = {
        "sender_id": user_id,
        "recipient_email": req.recipient_email,
        "record_id": req.record_id,
        "message": req.message,
    }

    try:
        response = client.table("shared_files").insert(share_data).execute()
        shared = response.data[0] if response.data else share_data
    except Exception as e:
        logger.error(f"Failed to share file: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to share file.",
        )

    return {
        "message": f"File shared with {req.recipient_email}",
        "shared_file": shared,
    }


@router.get("/inbox")
async def get_shared_inbox(user_id: str = Depends(get_current_user)):
    """
    View all files that have been shared with the authenticated user.
    Matches on the user's email address.
    """
    client = get_service_client()

    # Get the user's email from Supabase Auth
    user_response = client.auth.admin.get_user_by_id(user_id)
    if not user_response or not user_response.user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    user_email = user_response.user.email

    # Fetch shared files where recipient_email matches
    shared_response = (
        client.table("shared_files")
        .select("*, medical_records(*)")
        .eq("recipient_email", user_email)
        .order("created_at", desc=True)
        .execute()
    )

    return {
        "inbox": shared_response.data or [],
        "count": len(shared_response.data or []),
    }


@router.get("/inbox/list", include_in_schema=False)
async def get_shared_inbox_legacy(user_id: str = Depends(get_current_user)):
    """Legacy alias retained for backward compatibility with older clients."""
    return await get_shared_inbox(user_id)


@router.get("/{token}")
async def view_shared_record(token: str):
    """
    Public endpoint — doctor opens this link to view a patient's
    complete history and AI summary. No login required.
    """
    client = get_service_client()

    # ── Validate token ──
    token_response = (
        client.table("share_tokens")
        .select("*")
        .eq("token", token)
        .single()
        .execute()
    )

    if not token_response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid or expired share link.",
        )

    token_record = token_response.data

    # Check expiry
    expires_at = datetime.fromisoformat(token_record["expires_at"])
    if datetime.now(timezone.utc) > expires_at:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="This share link has expired.",
        )

    patient_id = token_record["patient_id"]

    # ── Fetch patient profile ──
    profile_response = (
        client.table("profiles")
        .select("*")
        .eq("id", patient_id)
        .single()
        .execute()
    )

    # ── Fetch all medical records ──
    records_response = (
        client.table("medical_records")
        .select("*")
        .eq("patient_id", patient_id)
        .order("created_at", desc=True)
        .execute()
    )

    # ── Fetch latest patient summary ──
    summary_response = (
        client.table("patient_summaries")
        .select("*")
        .eq("patient_id", patient_id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )

    # ── Fetch medicine analyses ──
    analyses_response = (
        client.table("medicine_analyses")
        .select("*")
        .eq("patient_id", patient_id)
        .order("created_at", desc=True)
        .execute()
    )

    return {
        "patient_profile": profile_response.data if profile_response.data else {},
        "medical_records": records_response.data or [],
        "latest_summary": summary_response.data[0] if summary_response.data else None,
        "medicine_analyses": analyses_response.data or [],
        "shared_at": token_record.get("created_at"),
        "expires_at": token_record["expires_at"],
    }
