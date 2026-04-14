"""
Configuration settings for database, API keys, and environment variables
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# API Keys and Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"

# Application Settings
DEBUG = os.getenv("DEBUG", "False") == "True"
