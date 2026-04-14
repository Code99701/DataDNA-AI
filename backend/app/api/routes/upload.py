"""
/upload endpoint - handles file uploads
"""
from fastapi import APIRouter, File, UploadFile

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file for watermarking and fingerprinting"""
    return {"filename": file.filename}
