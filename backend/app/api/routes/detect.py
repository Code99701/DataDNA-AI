"""
POST /detect — Accept a file, generate its hash, and find ownership in database.
"""

import logging
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.fingerprint import generate_fingerprint
from app.db.database import get_db
from app.db.models import DetectResponse, DetectMatch

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/detect", tags=["Detection"])


@router.post("/", response_model=DetectResponse)
async def detect_file(file: UploadFile = File(...)):
    """
    Check if a file exists in the system to verify ownership.
    """
    try:
        contents = await file.read()
    except Exception as exc:
        logger.exception("Failed to read uploaded file")
        raise HTTPException(status_code=400, detail="Could not read file")

    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    file_hash = generate_fingerprint(contents)
    db = get_db()
    
    # Check if hash exists in db
    match = await db.files.find_one({"hash": file_hash})

    if match:
        result = DetectMatch(
            file_id=match["file_id"],
            filename=match["filename"],
            owner_id=match["owner_id"],
            created_at=match["created_at"]
        )
        return DetectResponse(
            hash=file_hash,
            match_found=True,
            result=result,
            message=f"Match found. Owner: {match['owner_id']}"
        )
    return DetectResponse(
        hash=file_hash,
        match_found=False,
        result=None,
        message="No match found"
    )
