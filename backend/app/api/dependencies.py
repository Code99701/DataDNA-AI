"""
Dependency injection for API routes — authentication & authorization middleware.
"""

import logging
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.services.auth_service import decode_jwt
from app.db.database import get_db

logger = logging.getLogger(__name__)

# Bearer token extraction
security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """
    Extract and validate JWT from the Authorization header.
    Returns the full user document from the database.
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_jwt(credentials.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Fetch fresh user data from DB
    db = get_db()
    user = await db.users.find_one({"user_id": payload["sub"]})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists",
        )

    return user


async def require_2fa(
    current_user: dict = Depends(get_current_user),
) -> dict:
    """
    Ensure the current user has completed 2FA verification.
    Checks the JWT claims (decoded from token).
    """
    # Re-decode token to check 2FA claim
    # The user is already authenticated via get_current_user
    # We check the DB field as the source of truth
    if not current_user.get("is_2fa_verified", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Two-factor authentication required",
        )
    return current_user


async def require_admin(
    current_user: dict = Depends(require_2fa),
) -> dict:
    """
    Ensure the current user is an admin with 2FA verified.
    """
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


async def require_dashboard_access(
    current_user: dict = Depends(require_2fa),
) -> dict:
    """
    Ensure the current user has dashboard access granted.
    Admins always have access; regular users need explicit permission.
    """
    if current_user.get("role") == "admin":
        return current_user

    if not current_user.get("dashboard_access", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Dashboard access not granted. Contact an admin.",
        )
    return current_user
