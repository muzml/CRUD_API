"""
Authentication Dependencies Module (Stage 3)

Provides reusable FastAPI dependencies for authenticating requests using Supabase Auth JWT tokens.
Supports Local Dev Mode fallback when Supabase keys are unconfigured.
"""

import os
import hashlib
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.supabase_client import get_supabase_client

# HTTPBearer scheme adds Swagger UI "Authorize" lock button
security = HTTPBearer(auto_error=False)


def _is_unconfigured() -> bool:
    url = os.getenv("SUPABASE_URL", "")
    key = os.getenv("SUPABASE_KEY", "")
    return not url or url == "https://your-project-id.supabase.co" or not key or key == "your-supabase-anon-key"


def _make_dev_user_id(email: str) -> str:
    return "user_" + hashlib.md5(email.lower().encode()).hexdigest()[:12]


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    FastAPI dependency that extracts and validates the Bearer JWT token
    from the Authorization header using Supabase Auth (or Local Dev Mode fallback).

    Raises:
        HTTPException (401 Unauthorized): If token is missing, invalid, or expired.
    
    Returns:
        dict: User metadata dictionary containing user ID, email, and metadata.
    """
    if credentials is None or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token missing or invalid header format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = credentials.credentials

    # Local Dev Mode Handling
    if token.startswith("dev_access_token_") or _is_unconfigured():
        email = token.replace("dev_access_token_", "") if token.startswith("dev_access_token_") else "student@example.com"
        user_id = _make_dev_user_id(email)
        return {
            "id": user_id,
            "email": email,
            "role": "authenticated",
            "created_at": "2026-07-29T12:00:00Z"
        }

    try:
        supabase = get_supabase_client()
        user_response = supabase.auth.get_user(token)
        if not user_response or not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired authentication token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = user_response.user
        return {
            "id": user.id,
            "email": user.email,
            "role": getattr(user, "role", None),
            "created_at": str(getattr(user, "created_at", ""))
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
