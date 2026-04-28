"""
Pydantic models for authentication, user documents, and request/response schemas.
"""

from datetime import datetime, timezone
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from enum import Enum


# ── Enums ───────────────────────────────────────────────────
class AuthProvider(str, Enum):
    EMAIL = "email"
    GOOGLE = "google"


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


# ── Database document representation ────────────────────────
class UserDocument(BaseModel):
    """Schema stored in MongoDB `users` collection."""
    user_id: str = Field(..., description="Unique user identifier (UUID4)")
    email: str = Field(..., description="User email address")
    name: str = Field(default="", description="User display name")
    picture: str = Field(default="", description="Profile picture URL")
    auth_provider: AuthProvider = Field(default=AuthProvider.EMAIL, description="Auth provider")
    password_hash: str = Field(default="", description="bcrypt password hash (empty for Google users)")
    role: UserRole = Field(default=UserRole.USER, description="User role")
    dashboard_access: bool = Field(default=False, description="Whether user can access dashboard")
    is_2fa_verified: bool = Field(default=False, description="Whether 2FA is completed for current session")
    otp_code: str = Field(default="", description="Current OTP code")
    otp_expiry: Optional[datetime] = Field(default=None, description="OTP expiration timestamp")
    trusted_devices: List[str] = Field(default_factory=list, description="Trusted device fingerprints")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_login: Optional[datetime] = Field(default=None, description="Last login timestamp")


# ── API Request Models ──────────────────────────────────────
class RegisterRequest(BaseModel):
    email: str = Field(..., min_length=5, description="User email")
    password: str = Field(..., min_length=6, description="User password (min 6 chars)")
    name: str = Field(default="", description="Display name")


class LoginRequest(BaseModel):
    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")


class GoogleAuthRequest(BaseModel):
    credential: str = Field(..., description="Google ID token from GSI")


class OTPVerifyRequest(BaseModel):
    email: str = Field(..., description="User email")
    otp: str = Field(..., min_length=6, max_length=6, description="6-digit OTP code")


class ResendOTPRequest(BaseModel):
    email: str = Field(..., description="User email")


class UpdateRoleRequest(BaseModel):
    role: UserRole = Field(..., description="New role to assign")


class UpdateAccessRequest(BaseModel):
    dashboard_access: bool = Field(..., description="Grant or revoke dashboard access")


# ── API Response Models ─────────────────────────────────────
class AuthResponse(BaseModel):
    message: str
    token: Optional[str] = None
    user: Optional[dict] = None
    requires_otp: bool = False


class UserProfile(BaseModel):
    user_id: str
    email: str
    name: str
    picture: str
    role: UserRole
    auth_provider: AuthProvider
    dashboard_access: bool
    created_at: datetime
    last_login: Optional[datetime] = None


class UserListItem(BaseModel):
    user_id: str
    email: str
    name: str
    picture: str
    role: UserRole
    auth_provider: AuthProvider
    dashboard_access: bool
    created_at: datetime
    last_login: Optional[datetime] = None


class ActivityLogEntry(BaseModel):
    action: str
    admin_email: str
    target_email: str = ""
    details: str = ""
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
