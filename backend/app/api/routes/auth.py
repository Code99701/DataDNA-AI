"""
Authentication API routes — register, login, and Google OAuth.
"""

import uuid
import logging
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.database.database import get_db
from app.models.auth_models import (
    RegisterRequest,
    LoginRequest,
    GoogleAuthRequest,
    AuthResponse,
    UserProfile,
    AuthProvider,
    UserRole,
)
from app.services.auth_service import (
    hash_password,
    verify_password,
    create_jwt,
    verify_google_token,
)
from app.api.dependencies import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])

limiter = Limiter(key_func=get_remote_address)


# ── POST /auth/register ─────────────────────────────────────
@router.post("/register", response_model=AuthResponse)
@limiter.limit("5/minute")
async def register(request: Request, body: RegisterRequest):
    """Register a new user with email + password."""
    db = get_db()

    # Check if user already exists
    existing = await db.users.find_one({"email": body.email.lower()})
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    # Create user document
    user_id = str(uuid.uuid4())

    user_doc = {
        "user_id": user_id,
        "email": body.email.lower(),
        "name": body.name or body.email.split("@")[0],
        "picture": "",
        "auth_provider": AuthProvider.EMAIL.value,
        "password_hash": hash_password(body.password),
        "role": UserRole.USER.value,
        "dashboard_access": False,
        "is_2fa_verified": True,
        "trusted_devices": [],
        "created_at": datetime.now(timezone.utc),
        "last_login": None,
    }

    await db.users.insert_one(user_doc)

    logger.info("New user registered: %s", body.email)
    return AuthResponse(
        message="Account created successfully. You can now log in.",
        requires_otp=False,
    )


# ── POST /auth/login ────────────────────────────────────────
@router.post("/login", response_model=AuthResponse)
@limiter.limit("5/minute")
async def login(request: Request, body: LoginRequest):
    """Login with email + password."""
    db = get_db()

    user = await db.users.find_one({"email": body.email.lower()})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if user.get("auth_provider") == AuthProvider.GOOGLE.value:
        raise HTTPException(
            status_code=400,
            detail="This account uses Google Sign-In. Please use the Google button.",
        )

    if not verify_password(body.password, user.get("password_hash", "")):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_jwt(
        user_id=user["user_id"],
        email=user["email"],
        role=user["role"],
        is_2fa_verified=True,
        dashboard_access=user.get("dashboard_access", False),
    )

    await db.users.update_one(
        {"email": body.email.lower()},
        {"$set": {"last_login": datetime.now(timezone.utc)}},
    )

    logger.info("User logged in: %s", body.email)
    return AuthResponse(
        message="Login successful.",
        token=token,
        user={
            "user_id": user["user_id"],
            "email": user["email"],
            "name": user.get("name", ""),
            "picture": user.get("picture", ""),
            "role": user["role"],
            "dashboard_access": user.get("dashboard_access", False),
        },
        requires_otp=False,
    )


# ── POST /auth/google ───────────────────────────────────────
@router.post("/google", response_model=AuthResponse)
@limiter.limit("10/minute")
async def google_auth(request: Request, body: GoogleAuthRequest):
    """Authenticate via Google OAuth and return a JWT token."""
    db = get_db()

    # Verify Google token
    google_user = await verify_google_token(body.credential)
    if not google_user:
        raise HTTPException(status_code=401, detail="Invalid Google token")

    email = google_user["email"].lower()

    # Check if user exists
    user = await db.users.find_one({"email": email})

    if not user:
        # Auto-create user on first Google login
        user_id = str(uuid.uuid4())

        user_doc = {
            "user_id": user_id,
            "email": email,
            "name": google_user.get("name", email.split("@")[0]),
            "picture": google_user.get("picture", ""),
            "auth_provider": AuthProvider.GOOGLE.value,
            "password_hash": "",
            "role": UserRole.USER.value,
            "dashboard_access": False,
            "is_2fa_verified": True,
            "trusted_devices": [],
            "created_at": datetime.now(timezone.utc),
            "last_login": None,
        }

        await db.users.insert_one(user_doc)
        user = user_doc
        logger.info("New Google user created: %s", email)
    else:
        await db.users.update_one(
            {"email": email},
            {
                "$set": {
                    "picture": google_user.get("picture", user.get("picture", "")),
                    "name": google_user.get("name", user.get("name", "")),
                }
            },
        )

    token = create_jwt(
        user_id=user["user_id"],
        email=user["email"],
        role=user["role"],
        is_2fa_verified=True,
        dashboard_access=user.get("dashboard_access", False),
    )

    await db.users.update_one(
        {"email": email},
        {"$set": {"last_login": datetime.now(timezone.utc)}},
    )

    return AuthResponse(
        message="Login successful.",
        token=token,
        user={
            "user_id": user["user_id"],
            "email": user["email"],
            "name": user.get("name", ""),
            "picture": user.get("picture", ""),
            "role": user["role"],
            "dashboard_access": user.get("dashboard_access", False),
        },
        requires_otp=False,
    )


# ── GET /auth/me ─────────────────────────────────────────────
@router.get("/me", response_model=UserProfile)
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get the current authenticated user's profile."""
    return UserProfile(
        user_id=current_user["user_id"],
        email=current_user["email"],
        name=current_user.get("name", ""),
        picture=current_user.get("picture", ""),
        role=current_user["role"],
        auth_provider=current_user.get("auth_provider", "email"),
        dashboard_access=current_user.get("dashboard_access", False),
        created_at=current_user.get("created_at", datetime.now(timezone.utc)),
        last_login=current_user.get("last_login"),
    )
