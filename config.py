"""Application configuration constants."""

import os

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
DATABASE_PATH = os.getenv("DATABASE_PATH", "database.db")
