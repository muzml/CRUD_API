"""
Auth Service Module

Handles authentication logic interacting with Supabase Auth IdP, with local development fallback.
"""

import os
import hashlib
from typing import Dict, Any
from app.supabase_client import get_supabase_client
from app.schemas import AuthResponse


def _is_unconfigured() -> bool:
    url = os.getenv("SUPABASE_URL", "")
    key = os.getenv("SUPABASE_KEY", "")
    return not url or url == "https://your-project-id.supabase.co" or not key or key == "your-supabase-anon-key"


def _make_dev_user_id(email: str) -> str:
    return "user_" + hashlib.md5(email.lower().encode()).hexdigest()[:12]


class AuthService:
    """
    Service layer encapsulating Supabase Authentication workflows.
    Includes seamless Local Dev Mode fallback when Supabase keys are unconfigured.
    """

    @property
    def supabase(self):
        return get_supabase_client()

    def signup(self, email: str, password: str) -> Dict[str, Any]:
        """
        Registers a new user with Supabase Auth (or Local Dev Mode if unconfigured).
        """
        if _is_unconfigured():
            user_id = _make_dev_user_id(email)
            return {
                "message": "User registered successfully (Local Dev Mode).",
                "user_id": user_id,
                "email": email
            }

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
        Authenticates a user against Supabase Auth (or Local Dev Mode if unconfigured).
        """
        if _is_unconfigured():
            user_id = _make_dev_user_id(email)
            token = f"dev_access_token_{email}"
            return AuthResponse(
                access_token=token,
                refresh_token=f"dev_refresh_token_{email}",
                token_type="bearer",
                expires_in=3600,
                user_id=user_id,
                email=email
            )

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
        Exchanges a refresh token for a new access token session.
        """
        if not refresh_token or not refresh_token.strip():
            raise ValueError("Refresh token cannot be empty.")

        if _is_unconfigured():
            if not refresh_token.startswith("dev_refresh_token_"):
                raise ValueError("Invalid or expired refresh token.")
            email = refresh_token.replace("dev_refresh_token_", "")
            user_id = _make_dev_user_id(email)
            return AuthResponse(
                access_token=f"dev_access_token_{email}",
                refresh_token=refresh_token,
                token_type="bearer",
                expires_in=3600,
                user_id=user_id,
                email=email
            )

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
        Terminates the user session.
        """
        if not _is_unconfigured():
            try:
                self.supabase.auth.sign_out()
            except Exception:
                pass
        return {"message": "Successfully logged out."}
