"""
Supabase Client Initialization Module

Provides a singleton Supabase client instance initialized from environment variables.
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")


def get_supabase_client() -> Client:
    """
    Initializes and returns the Supabase client.
    Raises ValueError if environment variables are missing.
    """
    if not SUPABASE_URL or SUPABASE_URL == "https://your-project-id.supabase.co":
        raise ValueError("SUPABASE_URL environment variable is missing or unconfigured in .env file.")
    if not SUPABASE_KEY or SUPABASE_KEY == "your-supabase-anon-key":
        raise ValueError("SUPABASE_KEY environment variable is missing or unconfigured in .env file.")

    return create_client(SUPABASE_URL, SUPABASE_KEY)
