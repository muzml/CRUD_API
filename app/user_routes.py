"""
User Routes Module (Stage 2: Public & Protected Routes)

Defines GET /public/info and GET /protected/profile endpoints.
"""

from fastapi import APIRouter, Depends, status
from app.dependencies import get_current_user

router = APIRouter(tags=["Public & Protected Routes"])


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
def get_protected_profile(current_user: dict = Depends(get_current_user)):
    """
    Protected Profile Endpoint (GET /protected/profile)
    Requires a valid Bearer token in the Authorization header.
    Utilizes the reusable get_current_user dependency.
    """
    return {
        "message": "Welcome to your protected profile!",
        "user": current_user
    }

