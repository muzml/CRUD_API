"""
Auth Routes Module

Defines HTTP routes for User Signup and Login (POST /auth/signup, POST /auth/login).
"""

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from app.schemas import AuthCredentials, AuthResponse, RefreshTokenRequest
from app.auth_service import AuthService
from app.dependencies import get_current_user

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


@router.post("/refresh", response_model=AuthResponse, status_code=status.HTTP_200_OK)
def refresh_token(payload: RefreshTokenRequest):
    """
    Token Refresh Endpoint (POST /auth/refresh)
    Exchanges a valid refresh token for a new access token and refresh token session.
    """
    try:
        result = auth_service.refresh_session(payload.refresh_token)
        return result
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": str(e)}
        )


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(current_user: dict = Depends(get_current_user)):
    """
    User Logout Endpoint (POST /auth/logout)
    Terminates the user session on Supabase Auth.
    Requires a valid Bearer token in the Authorization header.
    """
    try:
        result = auth_service.logout()
        return result
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": str(e)}
        )

