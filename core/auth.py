"""
Authentication dependency — extracts and verifies the Supabase JWT
from the Authorization header.

Usage in any route:
    @router.get("/protected")
    async def protected(user_id: str = Depends(get_current_user)):
        ...
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.supabase_client import get_service_client

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """
    Verify the JWT token via Supabase's auth.getUser() endpoint.
    Returns the authenticated user's UUID string.
    """
    token = credentials.credentials

    try:
        # Use the service client to verify the token server-side
        client = get_service_client()
        user_response = client.auth.get_user(token)

        if user_response is None or user_response.user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )

        return str(user_response.user.id)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}",
        )
