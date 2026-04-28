"""
Application configuration loaded from environment variables.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── Application ─────────────────────────────────────────────
APP_TITLE = os.getenv("APP_TITLE", "DataDNA AI")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
APP_DESCRIPTION = os.getenv(
    "APP_DESCRIPTION",
    "File Ownership Fingerprinting System — upload, fingerprint, verify.",
)
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# ── MongoDB ─────────────────────────────────────────────────
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://sankalpshrivastava04_db_user:PASSWORD@cluster0.xq18vuf.mongodb.net/datadna")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "datadna")

# ── File Storage ────────────────────────────────────────────
STORAGE_DIR = os.getenv("STORAGE_DIR", os.path.join(os.getcwd(), "storage"))
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# ── Blockchain ──────────────────────────────────────────────
BLOCKCHAIN_FILE = os.getenv("BLOCKCHAIN_FILE", "blockchain.json")

# ── JWT Authentication ──────────────────────────────────────
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me-in-production-use-a-strong-random-key")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRY_HOURS = int(os.getenv("JWT_EXPIRY_HOURS", "24"))

# ── Google OAuth 2.0 ───────────────────────────────────────
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")

# ── SMTP (for OTP emails) ──────────────────────────────────
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")

# ── Logging ─────────────────────────────────────────────────
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ── Document Ownership Settings ─────────────────────────────
UPLOAD_TEMP_DIR = os.getenv("UPLOAD_TEMP_DIR", "storage/temp_uploads")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.8"))
CHUNK_ANALYSIS_LOW = float(os.getenv("CHUNK_ANALYSIS_LOW", "0.7"))
CHUNK_ANALYSIS_HIGH = float(os.getenv("CHUNK_ANALYSIS_HIGH", "0.85"))
PAGE_CHAR_LIMIT = int(os.getenv("PAGE_CHAR_LIMIT", "3000"))
REGISTRATION_SIMILARITY_BLOCK_THRESHOLD = float(
    os.getenv("REGISTRATION_SIMILARITY_BLOCK_THRESHOLD", "0.3")
)
