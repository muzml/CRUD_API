"""
Database Connection & Initialization Module

Manages connections to PostgreSQL (and SQLite for fallback) using environment variables.
"""

import os
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
