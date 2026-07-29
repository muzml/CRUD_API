"""
Auth Routes Module

Defines HTTP routes for User Signup and Login (POST /auth/signup, POST /auth/login).
"""

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.schemas import AuthCredentials, AuthResponse
from app.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])
auth_service = AuthService()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(payload: AuthCredentials):
    """
    User Signup Endpoint (POST /auth/signup)
    Registers a new user in Supabase Auth IdP.
    """
    try:
        result = auth_service.signup(payload.email, payload.password)
        return result
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": str(e)}
        )


@router.post("/login", response_model=AuthResponse, status_code=status.HTTP_200_OK)
def login(payload: AuthCredentials):
    """
    User Login Endpoint (POST /auth/login)
    Authenticates user against Supabase Auth and returns JWT tokens.
    """
    try:
        result = auth_service.login(payload.email, payload.password)
        return result
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": str(e)}
        )
