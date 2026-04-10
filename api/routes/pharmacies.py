"""
Pharmacy routes — nearby pharmacy search using Overpass API.

GET /api/pharmacies/nearby?lat=...&lon=...&radius_km=2
"""

from fastapi import APIRouter, Depends, Query
from core.auth import get_current_user
from services.overpass_service import find_nearby_pharmacies

router = APIRouter(prefix="/api/pharmacies", tags=["Pharmacies"])


@router.get("/nearby")
async def get_nearby_pharmacies(
    lat: float = Query(..., description="User's latitude"),
    lon: float = Query(..., description="User's longitude"),
    radius_km: float = Query(2.0, description="Search radius in km (default 2)"),
    user_id: str = Depends(get_current_user),
):
    """
    Find pharmacies near the user's location using OpenStreetMap data.
    Returns pharmacy name, coordinates, distance, and a Google Maps direction link.
    """
    pharmacies = await find_nearby_pharmacies(
        latitude=lat,
        longitude=lon,
        radius_km=radius_km,
    )

    return {
        "pharmacies": pharmacies,
        "count": len(pharmacies),
        "search_center": {"lat": lat, "lon": lon},
        "radius_km": radius_km,
    }
