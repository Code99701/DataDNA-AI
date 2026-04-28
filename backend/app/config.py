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

# Document Ownership Settings
UPLOAD_TEMP_DIR = os.getenv("UPLOAD_TEMP_DIR", "storage/temp_uploads")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.8"))
CHUNK_ANALYSIS_LOW = float(os.getenv("CHUNK_ANALYSIS_LOW", "0.7"))
CHUNK_ANALYSIS_HIGH = float(os.getenv("CHUNK_ANALYSIS_HIGH", "0.85"))
PAGE_CHAR_LIMIT = int(os.getenv("PAGE_CHAR_LIMIT", "3000"))

# If a new file being registered has >= this % total similarity to already
# registered documents, registration is blocked and a similarity report is
# returned instead (prevents re-registering merged/derived files as new).
REGISTRATION_SIMILARITY_BLOCK_THRESHOLD = float(
    os.getenv("REGISTRATION_SIMILARITY_BLOCK_THRESHOLD", "0.3")
)
