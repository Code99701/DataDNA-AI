"""
Pydantic models for request/response validation and MongoDB documents.
"""

from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# ── Database document representations ───────────────────────

class DocumentPageModel(BaseModel):
    """Schema for individual pages within a document."""
    page_number: int = Field(..., description="Page number (1-indexed)")
    page_hash: str = Field(..., description="SHA-256 hash of the normalized page text")
    embedding: Optional[bytes] = Field(default=None, description="Serialized 384-dim numpy array embedding")
    page_text: Optional[str] = Field(default=None, description="Raw text extracted from this page")


class RegisteredDocumentModel(BaseModel):
    """Schema stored in MongoDB `documents` collection."""
    file_id: str = Field(..., description="Unique file identifier (UUID4)")
    file_hash: str = Field(..., description="SHA-256 fingerprint of the complete file")
    filename: str = Field(..., description="Original uploaded filename")
    owner_id: str = Field(..., description="Owner's unique ID")
    owner_name: str = Field(..., description="Owner's display name")
    total_pages: int = Field(default=0, description="Total number of extracted text pages")
    registered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class BlockchainBlockModel(BaseModel):
    """Schema stored in MongoDB `blockchain_blocks` collection (mirror for fast queries)."""
    block_index: int = Field(..., description="Index of the block in the chain")
    block_hash: str = Field(..., description="SHA-256 hash of the block")
    previous_hash: str = Field(..., description="Hash of the previous block")
    file_hash: str = Field(..., description="Hash of the registered file")
    owner_name: str = Field(..., description="Name of the file owner")
    timestamp: datetime = Field(..., description="Time the block was created")


# ── API response models (Ownership) ─────────────────────────

class OwnerContribution(BaseModel):
    owner_id: str
    owner_name: str
    matched_documents: List[str]
    contribution: float
    pages_matched: int
    avg_similarity: float


class RegistrationResponse(BaseModel):
    status: str
    message: Optional[str] = None
    file_hash: str
    filename: Optional[str] = None
    owner_id: Optional[str] = None
    owner_name: Optional[str] = None
    total_pages: Optional[int] = None
    pages: Optional[List[Dict[str, Any]]] = None
    registered_at: Optional[str] = None
    blockchain: Optional[Dict[str, Any]] = None
    overall_similarity: Optional[float] = None
    dominant_owner: Optional[Dict[str, Any]] = None
    owners: Optional[List[OwnerContribution]] = None
    matched_pages: Optional[List[Dict[str, Any]]] = None
    unmatched_pages: Optional[List[int]] = None
    total_pages_analyzed: Optional[int] = None
    existing_owner: Optional[Dict[str, Any]] = None


class VerificationResponse(BaseModel):
    status: str
    message: str
    file_hash: str
    overall_similarity: float
    dominant_owner: Optional[Dict[str, Any]] = None
    owners: List[OwnerContribution] = []
    matched_pages: List[Dict[str, Any]] = []
    chunk_analysis: List[Dict[str, Any]] = []
    unmatched_pages: List[int] = []
    total_pages_analyzed: int
