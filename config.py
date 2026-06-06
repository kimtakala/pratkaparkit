import os

# Basic configuration values
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-change-me')
DATABASE_PATH = os.getenv('DATABASE_PATH', 'database.db')
