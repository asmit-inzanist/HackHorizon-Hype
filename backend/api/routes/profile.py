"""
Profile routes — create/update and get patient health profile.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from models.schemas import ProfileUpdate, ProfileResponse
from core.auth import get_current_user
from core.supabase_client import get_service_client

router = APIRouter(prefix="/api/profile", tags=["Profile"])


@router.get("", response_model=ProfileResponse)
async def get_profile(user_id: str = Depends(get_current_user)):
    """Get the authenticated user's health profile."""
    client = get_service_client()

    response = (
        client.table("profiles")
        .select("*")
        .eq("id", user_id)
        .single()
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found.",
        )

    return ProfileResponse(**response.data)


@router.put("", response_model=ProfileResponse)
async def update_profile(
    profile: ProfileUpdate,
    user_id: str = Depends(get_current_user),
):
    """Update the authenticated user's health profile."""
    client = get_service_client()

    # Build update dict, excluding None values
    update_data = profile.model_dump(exclude_none=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update.",
        )

    response = (
        client.table("profiles")
        .update(update_data)
        .eq("id", user_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found.",
        )

    return ProfileResponse(**response.data[0])
