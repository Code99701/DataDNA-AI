"""
/user endpoint - optional authentication and user management
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/user/profile")
async def get_user_profile():
    """Get user profile"""
    return {"user_id": None}
