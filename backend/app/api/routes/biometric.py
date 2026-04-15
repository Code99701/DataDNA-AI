from fastapi import APIRouter, UploadFile, File
import shutil
import os

from app.ai_models.biometric.preprocess import preprocess_image
from app.ai_models.biometric.fingerprint_model import get_fingerprint_embedding
from app.ai_models.biometric.matcher import match_fingerprints

router = APIRouter()

UPLOAD_DIR = "storage/biometric"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/verify-fingerprint")
async def verify_fingerprint(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    
    path1 = os.path.join(UPLOAD_DIR, file1.filename)
    path2 = os.path.join(UPLOAD_DIR, file2.filename)

    # Save files
    with open(path1, "wb") as f:
        shutil.copyfileobj(file1.file, f)

    with open(path2, "wb") as f:
        shutil.copyfileobj(file2.file, f)

    # Process images
    img1 = preprocess_image(path1)
    img2 = preprocess_image(path2)

    emb1 = get_fingerprint_embedding(img1)
    emb2 = get_fingerprint_embedding(img2)

    score = match_fingerprints(emb1, emb2)

    return {
        "similarity_score": score,
        "match": score > 0.9
    }