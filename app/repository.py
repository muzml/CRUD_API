from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any


class TaskRepository(ABC):
    """
    Abstract Base Class defining the contract for Task repository operations.
    Any database implementation (SQLite, PostgreSQL, Mock) must implement these methods.
    """

    @abstractmethod
    def get_all(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def create(self, title: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def update(self, task_id: int, title: Optional[str], done: Optional[bool]) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def delete(self, task_id: int) -> bool:
        pass


class PostgresTaskRepository(TaskRepository):
    """
    PostgreSQL Implementation of TaskRepository using psycopg2.
    """

    def __init__(self, get_connection_func):
        self.get_connection = get_connection_func

    def get_all(self) -> List[Dict[str, Any]]:
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, title, done FROM tasks ORDER BY id ASC;")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    def get_by_id(self, task_id: int) -> Optional[Dict[str, Any]]:
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, title, done FROM tasks WHERE id = %s;", (task_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            return dict(row)
        finally:
            conn.close()

    def create(self, title: str) -> Dict[str, Any]:
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id, title, done;",
                (title, False)
            )
            new_task = cursor.fetchone()
            conn.commit()
            return dict(new_task)
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def update(self, task_id: int, title: Optional[str], done: Optional[bool]) -> Optional[Dict[str, Any]]:
        existing_task = self.get_by_id(task_id)
        if existing_task is None:
            return None

        new_title = title if title is not None else existing_task["title"]
        new_done = done if done is not None else existing_task["done"]

        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING id, title, done;",
                (new_title, new_done, task_id)
            )
            updated_task = cursor.fetchone()
            conn.commit()
            return dict(updated_task)
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def delete(self, task_id: int) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM tasks WHERE id = %s;", (task_id,))
            affected_rows = cursor.rowcount
            conn.commit()
            return affected_rows > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()


class SQLiteTaskRepository(TaskRepository):
    """
    SQLite Implementation of TaskRepository for backwards compatibility.
    """

    def __init__(self, get_connection_func):
        self.get_connection = get_connection_func

    def get_all(self) -> List[Dict[str, Any]]:
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, title, done FROM tasks ORDER BY id ASC;")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    def get_by_id(self, task_id: int) -> Optional[Dict[str, Any]]:
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, title, done FROM tasks WHERE id = ?;", (task_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            return dict(row)
        finally:
            conn.close()

    def create(self, title: str) -> Dict[str, Any]:
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?);", (title, False))
            new_id = cursor.lastrowid
            conn.commit()
            return {"id": new_id, "title": title, "done": False}
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def update(self, task_id: int, title: Optional[str], done: Optional[bool]) -> Optional[Dict[str, Any]]:
        existing_task = self.get_by_id(task_id)
        if existing_task is None:
            return None

        new_title = title if title is not None else existing_task["title"]
        new_done = done if done is not None else existing_task["done"]

        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE tasks SET title = ?, done = ? WHERE id = ?;",
                (new_title, new_done, task_id)
            )
            conn.commit()
            return {"id": task_id, "title": new_title, "done": new_done}
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def delete(self, task_id: int) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM tasks WHERE id = ?;", (task_id,))
            affected_rows = cursor.rowcount
            conn.commit()
            return affected_rows > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
