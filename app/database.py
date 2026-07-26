"""
In-Memory Storage Module

This module simulates a database using a Python list.
Since no persistent database (like SQLite or PostgreSQL) is used, 
all data is stored in RAM and will reset whenever the FastAPI server restarts.
"""

from typing import Optional

# In-memory list to store task dictionaries
# Each task will look like: {"id": 1, "title": "Buy milk", "done": False}
tasks_db: list[dict] = []

# Counter for auto-generating unique task IDs
_id_counter: int = 1


def get_next_id() -> int:
    """Generates the next unique task ID (1, 2, 3...)."""
    global _id_counter
    current_id = _id_counter
    _id_counter += 1
    return current_id


def find_task_by_id(task_id: int) -> Optional[dict]:
    """Helper utility to find a task dictionary by its ID."""
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    return None
