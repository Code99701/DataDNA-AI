"""
GET /files — Return all stored file metadata for the dashboard.
"""

import logging
from fastapi import APIRouter, HTTPException, Query
from app.db.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/files", tags=["Files"])


@router.get("/")
async def list_files():
    """Return all file records from the database for the dashboard."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="Database is not connected")

    cursor = db.files.find({}, {"_id": 0})
    files = await cursor.to_list(length=500)
    total = await db.files.count_documents({})

    return {
        "total": total,
        "files": files,
    }


@router.get("/stats")
async def file_stats():
    """Return summary statistics for the dashboard."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="Database is not connected")

    total = await db.files.count_documents({})

    # Get the 2 most recent files for fingerprint preview
    cursor = db.files.find({}, {"_id": 0}).sort("created_at", -1).limit(2)
    recent = await cursor.to_list(length=2)

    return {
        "total_files": total,
        "recent_files": recent,
    }
