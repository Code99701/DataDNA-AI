"""
API routes for the Document Ownership Tracking and Verification system.

Endpoints:
  POST /ownership/register  — Register a document for ownership tracking
  POST /ownership/verify    — Verify a document against registered documents
  GET  /ownership/documents — List registered documents
  GET  /ownership/document/{file_hash} — Get details of a specific document
"""
import os
import shutil
import logging
from typing import Optional

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.api.dependencies import get_current_user
from app.models.auth_models import UserDocument

from app.config import UPLOAD_TEMP_DIR
from app.database.database import get_db

from app.services.registration_service import register_document
from app.services.verification_service import verify_document

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ownership", tags=["Document Ownership"])

# Ensure temp upload directory exists
os.makedirs(UPLOAD_TEMP_DIR, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}


def _get_file_extension(filename: str) -> str:
    """Extract and validate file extension."""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: .{ext}. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
        )
    return ext


def _save_temp_file(file: UploadFile) -> str:
    """Save uploaded file to temp directory and return the path."""
    file_path = os.path.join(UPLOAD_TEMP_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_path


def _cleanup_temp(file_path: str):
    """Remove temporary file after processing."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except OSError as e:
        logger.warning(f"Failed to clean up temp file {file_path}: {e}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# POST /ownership/register
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@router.post("/register")
async def register_file(
    file: UploadFile = File(...),
    owner_id: str = Form(...),
    owner_name: str = Form(...),
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: UserDocument = Depends(get_current_user),
):
    """
    Register a document for ownership tracking.

    Accepts a PDF, DOCX, or TXT file along with owner information.
    The system will:
    1. Hash the file to check for duplicates
    2. Extract text page-by-page
    3. Generate hashes and DL embeddings per page
    4. Store everything in the database

    Returns registration details or a duplicate notice.
    """
    # Validate file type
    file_ext = _get_file_extension(file.filename)

    # Save to temp
    file_path = _save_temp_file(file)

    try:
        result = await register_document(
            file_path=file_path,
            filename=file.filename,
            file_ext=file_ext,
            owner_id=owner_id,
            owner_name=owner_name,
            db=db,
        )
        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Registration failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")
    finally:
        _cleanup_temp(file_path)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# POST /ownership/verify
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@router.post("/verify")
async def verify_file(
    file: UploadFile = File(...),
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: UserDocument = Depends(get_current_user),
):
    """
    Verify a document against all registered documents.

    The system will:
    1. Check for exact file-level match (SHA-256)
    2. Check each page for exact hash matches
    3. Use DL embeddings for semantic similarity detection
    4. Perform chunk-level analysis for moderate matches
    5. Aggregate results with multi-owner attribution

    Returns a structured verification report.
    """
    # Validate file type
    file_ext = _get_file_extension(file.filename)

    # Save to temp
    file_path = _save_temp_file(file)

    try:
        result = await verify_document(
            file_path=file_path,
            filename=file.filename,
            file_ext=file_ext,
            db=db,
        )
        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Verification failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")
    finally:
        _cleanup_temp(file_path)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GET /ownership/documents
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@router.get("/documents")
async def list_documents(
    owner_id: Optional[str] = None,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: UserDocument = Depends(get_current_user),
):
    """
    List all registered documents, optionally filtered by owner.

    Query Parameters:
        owner_id: (optional) Filter documents by owner ID.
    """
    match = {}
    if owner_id:
        match["owner_id"] = owner_id
    documents = await db.documents.find(match).sort("registered_at", -1).to_list(length=None)

    return {
        "total": len(documents),
        "documents": [
            {
                "id": str(doc['_id']),
                "file_hash": doc['file_hash'],
                "filename": doc['filename'],
                "owner_id": doc['owner_id'],
                "owner_name": doc['owner_name'],
                "total_pages": doc['total_pages'],
                "registered_at": doc['registered_at'].isoformat(),
            }
            for doc in documents
        ],
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GET /ownership/document/{file_hash}
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@router.get("/document/{file_hash}")
async def get_document_details(
    file_hash: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: UserDocument = Depends(get_current_user),
):
    """
    Get detailed information about a specific registered document.

    Path Parameters:
        file_hash: The SHA-256 hash of the registered file.
    """
    doc = await db.documents.find_one({"file_hash": file_hash})

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    pages = (
        db.query(DocumentPage)
        .filter(DocumentPage.document_id == str(doc['_id']))
        .order_by(DocumentPage.page_number)
        .all()
    )

    return {
        "id": str(doc['_id']),
        "file_hash": doc['file_hash'],
        "filename": doc['filename'],
        "owner_id": doc['owner_id'],
        "owner_name": doc['owner_name'],
        "total_pages": doc['total_pages'],
        "registered_at": doc['registered_at'].isoformat(),
        "pages": [
            {
                "page_number": p['page_number'],
                "page_hash": p['page_hash'],
                "has_embedding": p.get('embedding') is not None,
                "text_preview": (p.get('page_text')[:200] + "...") if p.get('page_text') and len(p.get('page_text')) > 200 else p.get('page_text'),
            }
            for p in pages
        ],
    }
