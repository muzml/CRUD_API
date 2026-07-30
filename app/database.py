"""
Database Connection & Initialization Module

Manages connections to PostgreSQL (and SQLite for fallback) using environment variables.
"""

import os
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# PostgreSQL Connection Configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgrespassword@localhost:5432/taskdb"
)


def get_postgres_connection():
    """
    Creates and returns a connection to the PostgreSQL database.
    
    Using cursor_factory=RealDictCursor ensures query results are returned
    as dictionary-like objects matching key-value pairs (e.g. row['title']).
    """
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return conn


def get_sqlite_connection():
    """
    Creates and returns a connection to the local SQLite database as fallback when PostgreSQL is offline.
    """
    db_path = os.getenv("SQLITE_DB_PATH", "tasks.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0,
            user_id TEXT
        );
    """)
    conn.commit()
    return conn
