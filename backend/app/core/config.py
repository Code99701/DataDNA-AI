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
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "datadna")

# ── File Storage ────────────────────────────────────────────
STORAGE_DIR = os.getenv("STORAGE_DIR", os.path.join(os.getcwd(), "storage"))

# ── Blockchain ──────────────────────────────────────────────
BLOCKCHAIN_FILE = os.getenv("BLOCKCHAIN_FILE", "blockchain.json")

# ── Logging ─────────────────────────────────────────────────
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
