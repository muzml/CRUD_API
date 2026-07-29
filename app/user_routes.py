"""
User Routes Module (Stage 2: Public & Protected Routes)

Defines GET /public/info and GET /protected/profile endpoints.
"""

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from app.supabase_client import get_supabase_client

router = APIRouter(tags=["Public & Protected Routes"])
supabase = get_supabase_client()


@router.get("/public/info", status_code=status.HTTP_200_OK)
def get_public_info():
    """
    Public Info Endpoint (GET /public/info)
    Accessible by anyone without authentication.
    """
    return {
        "message": "This is a public endpoint accessible by anyone without authentication.",
        "status": "active",
        "access": "public"
    }


@router.get("/protected/profile", status_code=status.HTTP_200_OK)
def get_protected_profile(request: Request):
    """
    Protected Profile Endpoint (GET /protected/profile)
    Requires a valid Bearer token in the Authorization header.
    """
    # 1. Extract Authorization Header
    auth_header = request.headers.get("Authorization")

    # 2. Check for missing header
    if not auth_header:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Missing Authorization header"}
        )

    # 3. Check for correct 'Bearer <token>' format
    parts = auth_header.split(" ")
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Invalid Authorization header format. Expected 'Bearer <token>'"}
        )

    token = parts[1].strip()
    if not token:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Token string is empty"}
        )

    # 4. Verify token with Supabase Auth
    try:
        user_response = supabase.auth.get_user(token)
        if not user_response or not user_response.user:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": "Invalid or expired token"}
            )

        user = user_response.user
        return {
            "message": "Welcome to your protected profile!",
            "user": {
                "id": user.id,
                "email": user.email,
                "created_at": str(user.created_at),
                "role": user.role
            }
        }
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": f"Authentication failed: {str(e)}"}
        )
