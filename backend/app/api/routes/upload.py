from fastapi import APIRouter, UploadFile, File
import shutil
import os

from backend.app.services.fingerprint import create_datadna
from backend.app.services.watermark import embed_watermark

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = "storage/"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Generate fingerprint
    data = create_datadna()

    output_path = os.path.join(UPLOAD_DIR, "wm_" + file.filename)

    # Embed watermark
    embed_watermark(file_path, data["binary"], output_path)

    return {
        "message": "File processed",
        "fingerprint": data["fingerprint"],
        "watermarked_file": output_path
    }