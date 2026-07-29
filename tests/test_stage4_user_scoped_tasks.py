import sys
import os
import asyncio
import httpx

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app, get_task_service
from app.dependencies import get_current_user
from app.service import TaskService
from app.repository import TaskRepository


class MockInMemoryTaskRepository(TaskRepository):
    """In-memory mock task repository for fast isolated multi-tenant testing."""
    def __init__(self):
        self.tasks = []
        self.counter = 1

    def get_all(self, user_id=None):
        if user_id:
            return [t for t in self.tasks if t.get("user_id") == user_id or t.get("user_id") is None]
        return list(self.tasks)

    def get_by_id(self, task_id: int, user_id=None):
        for t in self.tasks:
            if t["id"] == task_id:
                if user_id and t.get("user_id") not in (user_id, None):
                    return None
                return dict(t)
        return None

    def create(self, title: str, user_id=None):
        task = {
            "id": self.counter,
            "title": title,
            "done": False,
            "user_id": user_id
        }
        self.counter += 1
        self.tasks.append(task)
        return dict(task)

    def update(self, task_id: int, title=None, done=None, user_id=None):
        task = self.get_by_id(task_id, user_id=user_id)
        if not task:
            return None
        for t in self.tasks:
            if t["id"] == task_id:
                if title is not None:
                    t["title"] = title
                if done is not None:
                    t["done"] = done
                return dict(t)
        return None

    def delete(self, task_id: int, user_id=None):
        task = self.get_by_id(task_id, user_id=user_id)
        if not task:
            return False
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        return True


async def run_stage4_tests():
    print("Running Stage 4 User-Scoped Data Isolation Tests...")

    # Override get_task_service to use our mock repository
    mock_repo = MockInMemoryTaskRepository()
    mock_service = TaskService(mock_repo)
    app.dependency_overrides[get_task_service] = lambda: mock_service

    user_a = {"id": "user-aaa-111", "email": "usera@example.com"}
    user_b = {"id": "user-bbb-222", "email": "userb@example.com"}

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        
        # 1. User A creates a task
        app.dependency_overrides[get_current_user] = lambda: user_a
        res_a = await client.post("/tasks", json={"title": "User A Private Task"})
        assert res_a.status_code == 201, f"Expected 201, got {res_a.status_code}"
        task_a_id = res_a.json()["id"]
        assert res_a.json()["user_id"] == "user-aaa-111"
        print("[PASS] Test 1: User A created Task 1 (user_id=user-aaa-111)")

        # 2. User B creates a task
        app.dependency_overrides[get_current_user] = lambda: user_b
        res_b = await client.post("/tasks", json={"title": "User B Private Task"})
        assert res_b.status_code == 201, f"Expected 201, got {res_b.status_code}"
        task_b_id = res_b.json()["id"]
        assert res_b.json()["user_id"] == "user-bbb-222"
        print("[PASS] Test 2: User B created Task 2 (user_id=user-bbb-222)")

        # 3. User A lists tasks -> sees Task 1, does NOT see Task 2
        app.dependency_overrides[get_current_user] = lambda: user_a
        list_a = await client.get("/tasks")
        assert list_a.status_code == 200
        titles_a = [t["title"] for t in list_a.json()]
        assert "User A Private Task" in titles_a
        assert "User B Private Task" not in titles_a
        print("[PASS] Test 3: User A list endpoint returns ONLY User A tasks")

        # 4. User B attempts to access User A's task -> 404 Not Found
        app.dependency_overrides[get_current_user] = lambda: user_b
        get_other = await client.get(f"/tasks/{task_a_id}")
        assert get_other.status_code == 404
        print("[PASS] Test 4: User B requesting GET /tasks/{User A Task ID} receives 404 Not Found")

        # 5. User B attempts to update User A's task -> 404 Not Found
        update_other = await client.put(f"/tasks/{task_a_id}", json={"done": True})
        assert update_other.status_code == 404
        print("[PASS] Test 5: User B requesting PUT /tasks/{User A Task ID} receives 404 Not Found")

        # 6. User B attempts to delete User A's task -> 404 Not Found
        delete_other = await client.delete(f"/tasks/{task_a_id}")
        assert delete_other.status_code == 404
        print("[PASS] Test 6: User B requesting DELETE /tasks/{User A Task ID} receives 404 Not Found")

        # 7. User A can update and delete their own task successfully
        app.dependency_overrides[get_current_user] = lambda: user_a
        update_own = await client.put(f"/tasks/{task_a_id}", json={"done": True})
        assert update_own.status_code == 200
        assert update_own.json()["done"] is True
        print("[PASS] Test 7: User A can successfully update own task")

        delete_own = await client.delete(f"/tasks/{task_a_id}")
        assert delete_own.status_code == 204
        print("[PASS] Test 8: User A can successfully delete own task")

    app.dependency_overrides.clear()
    print("\nALL STAGE 4 MULTI-TENANT ISOLATION TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    asyncio.run(run_stage4_tests())
