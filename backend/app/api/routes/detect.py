from fastapi import APIRouter, UploadFile, File
import shutil
import os

from app.services.extraction import extract_watermark

router = APIRouter(prefix="/detect", tags=["Detect"])

UPLOAD_DIR = "storage/"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/")
async def detect_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract fingerprint
    extracted = extract_watermark(file_path)

    return {
        "extracted_fingerprint": extracted
    }