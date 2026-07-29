"""
Auth Service Module

Handles authentication logic interacting with Supabase Auth IdP.
"""

from typing import Dict, Any
from app.supabase_client import get_supabase_client
from app.schemas import AuthResponse


class AuthService:
    """
    Service layer encapsulating Supabase Authentication workflows.
    """

    @property
    def supabase(self):
        return get_supabase_client()

    def signup(self, email: str, password: str) -> Dict[str, Any]:
        """
        Registers a new user with Supabase Auth.
        """
        response = self.supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        if not response.user:
            raise ValueError("Signup failed: Could not create user.")

        return {
            "message": "User registered successfully.",
            "user_id": response.user.id,
            "email": response.user.email
        }

    def login(self, email: str, password: str) -> AuthResponse:
        """
        Authenticates a user against Supabase Auth and returns JWT tokens.
        """
        response = self.supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        if not response.session or not response.user:
            raise ValueError("Invalid email or password.")

        return AuthResponse(
            access_token=response.session.access_token,
            refresh_token=response.session.refresh_token,
            token_type="bearer",
            expires_in=response.session.expires_in,
            user_id=response.user.id,
            email=response.user.email
        )

    def refresh_session(self, refresh_token: str) -> AuthResponse:
        """
        Exchanges a refresh token for a new access token and refresh token session.
        """
        response = self.supabase.auth.refresh_session(refresh_token)

        if not response.session or not response.user:
            raise ValueError("Invalid or expired refresh token.")

        return AuthResponse(
            access_token=response.session.access_token,
            refresh_token=response.session.refresh_token,
            token_type="bearer",
            expires_in=response.session.expires_in,
            user_id=response.user.id,
            email=response.user.email
        )

    def logout(self) -> Dict[str, str]:
        """
        Terminates the user session on Supabase Auth.
        """
        self.supabase.auth.sign_out()
        return {"message": "Successfully logged out."}

