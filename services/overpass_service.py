"""
Overpass API Service — find nearby pharmacies using OpenStreetMap data.
Free, no API key required.
"""

import httpx
import math
import logging

logger = logging.getLogger(__name__)

OVERPASS_URL = "https://overpass-api.de/api/interpreter"


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great-circle distance between two points in km."""
    R = 6371.0  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


async def find_nearby_pharmacies(
    latitude: float,
    longitude: float,
    radius_km: float = 2.0,
) -> list[dict]:
    """
    Query Overpass API for pharmacies within `radius_km` of the given coordinates.

    Args:
        latitude: User's GPS latitude.
        longitude: User's GPS longitude.
        radius_km: Search radius in kilometers (default 2km).

    Returns:
        List of pharmacy dicts with name, lat, lon, address, distance, directions_url.
    """
    radius_m = int(radius_km * 1000)

    # Overpass QL query for pharmacies
    query = f"""
    [out:json][timeout:10];
    (
      node["amenity"="pharmacy"](around:{radius_m},{latitude},{longitude});
      way["amenity"="pharmacy"](around:{radius_m},{latitude},{longitude});
      relation["amenity"="pharmacy"](around:{radius_m},{latitude},{longitude});
    );
    out center body;
    """

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                OVERPASS_URL,
                data={"data": query},
            )
            response.raise_for_status()
            data = response.json()

    except httpx.HTTPError as e:
        logger.error(f"Overpass API error: {e}")
        return []

    pharmacies = []
    for element in data.get("elements", []):
        # Get coordinates — nodes have lat/lon directly, ways/relations use center
        lat = element.get("lat") or element.get("center", {}).get("lat")
        lon = element.get("lon") or element.get("center", {}).get("lon")

        if lat is None or lon is None:
            continue

        tags = element.get("tags", {})
        name = tags.get("name", tags.get("name:en", "Unnamed Pharmacy"))

        # Build address from available tags
        address_parts = []
        for key in ["addr:street", "addr:housenumber", "addr:city", "addr:postcode"]:
            if key in tags:
                address_parts.append(tags[key])
        address = ", ".join(address_parts) if address_parts else None

        # Calculate distance
        distance = _haversine_km(latitude, longitude, lat, lon)

        # Google Maps directions URL (free to link, no API needed)
        directions_url = (
            f"https://www.google.com/maps/dir/?api=1"
            f"&origin={latitude},{longitude}"
            f"&destination={lat},{lon}"
            f"&travelmode=walking"
        )

        pharmacies.append({
            "name": name,
            "latitude": lat,
            "longitude": lon,
            "address": address,
            "distance_km": round(distance, 2),
            "directions_url": directions_url,
        })

    # Sort by distance
    pharmacies.sort(key=lambda p: p["distance_km"])

    logger.info(f"Found {len(pharmacies)} pharmacies within {radius_km}km")
    return pharmacies
