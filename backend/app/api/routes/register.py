from fastapi import APIRouter, UploadFile, File
import uuid
import os
from app.services.fingerprint import generate_fingerprint

router = APIRouter()

STORAGE_DIR = "storage/fingerprints"
os.makedirs(STORAGE_DIR, exist_ok=True)

@router.post("/register-fingerprint")
async def register_fingerprint(file: UploadFile = File(...)):
    contents = await file.read()

    file_path = f"{STORAGE_DIR}/{uuid.uuid4()}.png"

    with open(file_path, "wb") as f:
        f.write(contents)

    fingerprint = generate_fingerprint(contents)

    return {
        "message": "Fingerprint Registered",
        "fingerprint_id": fingerprint
    }