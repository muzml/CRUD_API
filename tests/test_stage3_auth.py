import sys
import os
import asyncio
import httpx

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.dependencies import get_current_user


async def run_all_tests():
    print("Running Stage 3 Authentication Integration Tests...")

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        
        # 1. Test Public Info Endpoint
        res = await client.get("/public/info")
        assert res.status_code == 200, f"Expected 200, got {res.status_code}"
        assert res.json()["access"] == "public"
        print("[PASS] Test 1: GET /public/info is publicly accessible (200 OK)")

        # 2. Test Protected Profile Without Token
        res = await client.get("/protected/profile")
        assert res.status_code == 401, f"Expected 401, got {res.status_code}"
        print("[PASS] Test 2: GET /protected/profile without token returns 401 Unauthorized")

        # 3. Test Tasks Endpoints Without Token
        res = await client.get("/tasks")
        assert res.status_code == 401, f"Expected 401, got {res.status_code}"
        print("[PASS] Test 3: GET /tasks without token returns 401 Unauthorized")

        res = await client.get("/tasks/1")
        assert res.status_code == 401, f"Expected 401, got {res.status_code}"
        print("[PASS] Test 4: GET /tasks/1 without token returns 401 Unauthorized")

        res = await client.post("/tasks", json={"title": "Test Task"})
        assert res.status_code == 401, f"Expected 401, got {res.status_code}"
        print("[PASS] Test 5: POST /tasks without token returns 401 Unauthorized")

        res = await client.put("/tasks/1", json={"done": True})
        assert res.status_code == 401, f"Expected 401, got {res.status_code}"
        print("[PASS] Test 6: PUT /tasks/1 without token returns 401 Unauthorized")

        res = await client.delete("/tasks/1")
        assert res.status_code == 401, f"Expected 401, got {res.status_code}"
        print("[PASS] Test 7: DELETE /tasks/1 without token returns 401 Unauthorized")

        # 4. Test Protected Profile & Tasks with Authorized User (Dependency Override)
        mock_user = {
            "id": "12345678-1234-1234-1234-123456789abc",
            "email": "testuser@example.com",
            "role": "authenticated",
            "created_at": "2026-07-29T12:00:00Z"
        }

        app.dependency_overrides[get_current_user] = lambda: mock_user

        try:
            res = await client.get("/protected/profile")
            assert res.status_code == 200, f"Expected 200, got {res.status_code}"
            assert res.json()["user"]["email"] == "testuser@example.com"
            print("[PASS] Test 8: GET /protected/profile with authorized token returns 200 OK & user data")
        finally:
            app.dependency_overrides.clear()

    print("\nALL STAGE 3 TESTS PASSED SUCCESSFULLY!")



if __name__ == "__main__":
    asyncio.run(run_all_tests())
