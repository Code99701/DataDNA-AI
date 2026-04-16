"""
POST /upload — Accept a file, fingerprint it, store it, and record on blockchain.
"""

import logging
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.fingerprint import generate_fingerprint
from app.services.storage import save_file
from app.services.blockchain import blockchain
from app.db.database import get_db
from app.db.models import FileDocument, UploadResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/", response_model=UploadResponse, status_code=201)
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a file to DataDNA AI.

    - Generates SHA-256 fingerprint
    - Saves file to local storage
    - Stores metadata in MongoDB
    - Records hash on the blockchain
    """
    try:
        contents = await file.read()
    except Exception as exc:
        logger.exception("Failed to read uploaded file")
        raise HTTPException(status_code=400, detail=f"Could not read file: {exc}")

    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    # 1. Fingerprint
    file_hash = generate_fingerprint(contents)

    # 2. Save to disk
    file_id, stored_path = save_file(file.filename, contents)

    # 3. Store metadata in MongoDB
    doc = FileDocument(
        file_id=file_id,
        filename=file.filename,
        hash=file_hash,
        owner_id="owner_default",
        path=stored_path,
    )
    db = get_db()
    await db.files.insert_one(doc.model_dump())
    logger.info("Metadata stored for file_id=%s", file_id)

    # 4. Record on blockchain
    block = blockchain.add_block(file_hash)

    return UploadResponse(
        file_id=file_id,
        hash=file_hash,
        blockchain_index=block.index,
        message="File stored successfully",
    )