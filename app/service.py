"""
Task Service Module

Contains business logic for Task management. Serves as the intermediary
between HTTP Route Handlers (FastAPI) and the Database Repository layer.
"""

from typing import List, Optional, Dict, Any
from app.repository import TaskRepository


class TaskService:
    """
    TaskService encapsulates application business rules.
    Decoupled from specific database drivers by depending on the TaskRepository interface.
    Supports user ownership scoping.
    """

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def list_tasks(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieves all tasks scoped to a specific user_id."""
        return self.repository.get_all(user_id=user_id)

    def get_task(self, task_id: int, user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Retrieves a single task by ID scoped to user_id."""
        return self.repository.get_by_id(task_id, user_id=user_id)

    def create_task(self, title: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Creates a new task bound to user_id."""
        return self.repository.create(title, user_id=user_id)

    def update_task(self, task_id: int, title: Optional[str], done: Optional[bool], user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Updates an existing task owned by user_id."""
        return self.repository.update(task_id, title, done, user_id=user_id)

    def delete_task(self, task_id: int, user_id: Optional[str] = None) -> bool:
        """Deletes a task by ID owned by user_id."""
        return self.repository.delete(task_id, user_id=user_id)
