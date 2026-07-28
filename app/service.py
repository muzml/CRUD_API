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
    """

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def list_tasks(self) -> List[Dict[str, Any]]:
        """Retrieves all tasks."""
        return self.repository.get_all()

    def get_task(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves a single task by ID."""
        return self.repository.get_by_id(task_id)

    def create_task(self, title: str) -> Dict[str, Any]:
        """Creates a new task."""
        return self.repository.create(title)

    def update_task(self, task_id: int, title: Optional[str], done: Optional[bool]) -> Optional[Dict[str, Any]]:
        """Updates an existing task."""
        return self.repository.update(task_id, title, done)

    def delete_task(self, task_id: int) -> bool:
        """Deletes a task by ID."""
        return self.repository.delete(task_id)
