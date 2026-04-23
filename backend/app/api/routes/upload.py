"""POST /upload — fingerprint, store, and record ownership hash."""

import logging

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.db.database import get_db
from app.db.models import FileDocument, UploadResponse
from app.services.blockchain import blockchain
from app.services.fingerprint import generate_fingerprint
from app.services.storage import save_file

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/", response_model=UploadResponse, status_code=201)
async def upload_file(file: UploadFile = File(...), owner: str = Form("owner_default")):
    """Upload file and produce: file -> hash -> stored -> blockchain record."""
    try:
        contents = await file.read()
    except Exception as exc:
        logger.exception("Failed to read uploaded file")
        raise HTTPException(status_code=400, detail=f"Could not read file: {exc}")

    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    # 1) Fingerprint
    file_hash = generate_fingerprint(contents)

    # 2) Persist (GCS preferred, local fallback)
    file_id, stored_path, storage_provider = save_file(file.filename, contents)

    # 3) Store metadata
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="Database is not connected")

    doc = FileDocument(
        file_id=file_id,
        filename=file.filename,
        hash=file_hash,
        owner_id=owner,
        path=stored_path,
        storage_provider=storage_provider,
    )
    await db.files.insert_one(doc.model_dump())
    logger.info("Metadata stored for file_id=%s", file_id)

    # 4) Record ownership hash on blockchain (hash-chain)
    block = blockchain.add_block(file_hash)

    return UploadResponse(
        file_id=file_id,
        hash=file_hash,
        storage_provider=storage_provider,
        storage_path=stored_path,
        blockchain_index=block.index,
        message="File hashed, stored, and recorded successfully",
    )
