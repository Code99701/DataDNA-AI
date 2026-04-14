"""
/detect endpoint - detects watermarks and generates fingerprints
"""
from fastapi import APIRouter

router = APIRouter()

@router.post("/detect")
async def detect_watermark():
    """Detect watermark in file"""
    return {"detected": False}
