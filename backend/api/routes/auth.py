"""
Auth routes — signup and login via Supabase Auth.
"""

from fastapi import APIRouter, HTTPException, status
from models.schemas import SignupRequest, LoginRequest, AuthResponse
from core.supabase_client import get_anon_client

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/signup", response_model=AuthResponse)
async def signup(req: SignupRequest):
    """Register a new user. A profile is auto-created via the DB trigger."""
    client = get_anon_client()

    try:
        response = client.auth.sign_up({
            "email": req.email,
            "password": req.password,
        })

        if response.user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Signup failed — user may already exist.",
            )

        return AuthResponse(
            access_token=response.session.access_token if response.session else "",
            user_id=str(response.user.id),
            email=response.user.email or req.email,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Signup error: {str(e)}",
        )


@router.post("/login", response_model=AuthResponse)
async def login(req: LoginRequest):
    """Login with email and password. Returns a JWT access token."""
    client = get_anon_client()

    try:
        response = client.auth.sign_in_with_password({
            "email": req.email,
            "password": req.password,
        })

        if response.user is None or response.session is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        return AuthResponse(
            access_token=response.session.access_token,
            user_id=str(response.user.id),
            email=response.user.email or req.email,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Login error: {str(e)}",
        )
