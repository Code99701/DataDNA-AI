"""
Pydantic models for request/response validation and MongoDB documents.
"""

from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field


# ── Database document representation ────────────────────────
class FileDocument(BaseModel):
    """Schema stored in MongoDB `files` collection."""
    file_id: str = Field(..., description="Unique file identifier (UUID4)")
    filename: str = Field(..., description="Original uploaded filename")
    hash: str = Field(..., description="SHA-256 fingerprint of file contents")
    owner_id: str = Field(default="owner_default", description="Owner identifier")
    path: str = Field(..., description="Relative storage path on disk")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ── API response models ─────────────────────────────────────
class UploadResponse(BaseModel):
    file_id: str
    hash: str
    blockchain_index: Optional[int] = None
    message: str = "File stored successfully"


class DetectMatch(BaseModel):
    file_id: str
    filename: str
    owner_id: str
    confidence: float = 1.0
    created_at: datetime


class DetectResponse(BaseModel):
    hash: str
    match_found: bool
    result: Optional[DetectMatch] = None
    message: str
