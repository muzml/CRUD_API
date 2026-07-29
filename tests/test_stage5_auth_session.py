import sys
import os
import asyncio
import httpx

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.dependencies import get_current_user
from app.auth_routes import auth_service


async def run_stage5_tests():
    print("Running Stage 5 Session Management Tests...")

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:

        # 1. Test POST /auth/refresh with empty payload -> 400 Bad Request
        res_empty = await client.post("/auth/refresh", json={"refresh_token": "   "})
        assert res_empty.status_code == 400, f"Expected 400, got {res_empty.status_code}"
        print("[PASS] Test 1: POST /auth/refresh with empty token returns 400 Bad Request")

        # 2. Test POST /auth/refresh with invalid token -> 400 Bad Request
        res_invalid = await client.post("/auth/refresh", json={"refresh_token": "invalid.refresh.token"})
        assert res_invalid.status_code == 400, f"Expected 400, got {res_invalid.status_code}"
        print("[PASS] Test 2: POST /auth/refresh with invalid token returns 400 Bad Request")

        # 3. Test POST /auth/logout without Bearer token -> 401 Unauthorized
        res_logout_unauth = await client.post("/auth/logout")
        assert res_logout_unauth.status_code == 401, f"Expected 401, got {res_logout_unauth.status_code}"
        print("[PASS] Test 3: POST /auth/logout without token returns 401 Unauthorized")

        # 4. Test POST /auth/logout with authorized user -> 200 OK
        mock_user = {"id": "user-logout-123", "email": "logout@example.com"}
        app.dependency_overrides[get_current_user] = lambda: mock_user

        # Mock auth_service.logout to avoid unconfigured Supabase SDK network call
        original_logout = auth_service.logout
        auth_service.logout = lambda: {"message": "Successfully logged out."}

        try:
            res_logout_auth = await client.post("/auth/logout")
            assert res_logout_auth.status_code == 200, f"Expected 200, got {res_logout_auth.status_code}"
            assert res_logout_auth.json()["message"] == "Successfully logged out."
            print("[PASS] Test 4: POST /auth/logout with valid token returns 200 OK & logout message")
        finally:
            auth_service.logout = original_logout
            app.dependency_overrides.clear()

        # 5. Test Mocked Token Refresh flow returning valid AuthResponse
        original_refresh = auth_service.refresh_session
        auth_service.refresh_session = lambda token: {
            "access_token": "new.access.token",
            "refresh_token": "new.refresh.token",
            "token_type": "bearer",
            "expires_in": 3600,
            "user_id": "user-refresh-123",
            "email": "refreshed@example.com"
        }

        try:
            res_refreshed = await client.post("/auth/refresh", json={"refresh_token": "valid.mock.token"})
            assert res_refreshed.status_code == 200
            data = res_refreshed.json()
            assert data["access_token"] == "new.access.token"
            assert data["user_id"] == "user-refresh-123"
            print("[PASS] Test 5: POST /auth/refresh with valid token returns new AuthResponse")
        finally:
            auth_service.refresh_session = original_refresh

    print("\nALL STAGE 5 SESSION MANAGEMENT TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    asyncio.run(run_stage5_tests())
