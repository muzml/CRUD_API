"""
SQLite Database Module

This module manages the connection to the SQLite database (tasks.db)
and handles database initialization, table creation, and initial data seeding.
"""

import sqlite3

# Constant defining the path to the SQLite database file
DB_PATH = "tasks.db"


def get_db_connection() -> sqlite3.Connection:
    """
    Creates and returns a new connection to the SQLite database.
    
    Setting row_factory to sqlite3.Row allows accessing query columns
    by name (e.g., row['title']) like a dictionary rather than tuple indexes.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """
    Initializes the database:
    1. Creates the 'tasks' table if it does not exist.
    2. Seeds 3 default tasks if the table is empty.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Create table statement
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        );
    """)

    # 2. Check if the table is empty
    cursor.execute("SELECT COUNT(*) FROM tasks;")
    count = cursor.fetchone()[0]

    # 3. Seed initial data only if empty
    if count == 0:
        seed_tasks = [
            ("Buy groceries", False),
            ("Read SQLite documentation", False),
            ("Build FastAPI application", True)
        ]
        cursor.executemany("""
            INSERT INTO tasks (title, done)
            VALUES (?, ?);
        """, seed_tasks)

    # Commit changes and close the connection
    conn.commit()
    conn.close()
