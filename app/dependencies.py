"""
Authentication Dependencies Module (Stage 3)

Provides reusable FastAPI dependencies for authenticating requests using Supabase Auth JWT tokens.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.supabase_client import get_supabase_client

# HTTPBearer scheme adds Swagger UI "Authorize" lock button
security = HTTPBearer(auto_error=False)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    FastAPI dependency that extracts and validates the Bearer JWT token
    from the Authorization header using Supabase Auth.

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
