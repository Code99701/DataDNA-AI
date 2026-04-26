"""
Core authentication service — password hashing, JWT tokens, OTP, Google OAuth,
and email delivery.
"""

import secrets
import logging
from datetime import datetime, timezone, timedelta
from typing import Optional

import bcrypt
import jwt
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests

from app.core.config import (
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
    JWT_EXPIRY_HOURS,
    GOOGLE_CLIENT_ID,
    SMTP_HOST,
    SMTP_PORT,
    SMTP_USER,
    SMTP_PASS,
)

logger = logging.getLogger(__name__)


# ── Password Hashing ────────────────────────────────────────
def hash_password(password: str) -> str:
    """Hash a plaintext password with bcrypt."""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    """Verify a plaintext password against a bcrypt hash."""
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


# ── JWT Tokens ──────────────────────────────────────────────
def create_jwt(
    user_id: str,
    email: str,
    role: str,
    is_2fa_verified: bool = False,
    dashboard_access: bool = False,
) -> str:
    """Create a signed JWT token."""
    payload = {
        "sub": user_id,
        "email": email,
        "role": role,
        "is_2fa_verified": is_2fa_verified,
        "dashboard_access": dashboard_access,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRY_HOURS),
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_jwt(token: str) -> Optional[dict]:
    """Decode and validate a JWT token. Returns payload or None."""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("JWT token expired")
        return None
    except jwt.InvalidTokenError as e:
        logger.warning("Invalid JWT token: %s", e)
        return None


# ── OTP Generation ──────────────────────────────────────────
def generate_otp() -> tuple[str, datetime]:
    """Generate a 6-digit OTP and its expiry (5 minutes from now)."""
    otp = "".join([str(secrets.randbelow(10)) for _ in range(6)])
    expiry = datetime.now(timezone.utc) + timedelta(minutes=5)
    return otp, expiry


def verify_otp(stored_otp: str, stored_expiry: datetime, provided_otp: str) -> bool:
    """Verify OTP code and check it hasn't expired."""
    if not stored_otp or not stored_expiry:
        return False
    
    if stored_expiry.tzinfo is None:
        stored_expiry = stored_expiry.replace(tzinfo=timezone.utc)
        
    if datetime.now(timezone.utc) > stored_expiry:
        return False
    return secrets.compare_digest(stored_otp, provided_otp)


# ── Google OAuth Token Verification ─────────────────────────
async def verify_google_token(credential: str) -> Optional[dict]:
    """
    Verify a Google ID token and return user info.
    Returns dict with: email, name, picture, sub (Google user ID)
    """
    try:
        idinfo = google_id_token.verify_oauth2_token(
            credential,
            google_requests.Request(),
            GOOGLE_CLIENT_ID,
        )
        # Verify issuer
        if idinfo["iss"] not in ("accounts.google.com", "https://accounts.google.com"):
            logger.error("Google token has invalid issuer: %s", idinfo["iss"])
            return None

        return {
            "email": idinfo.get("email", ""),
            "name": idinfo.get("name", ""),
            "picture": idinfo.get("picture", ""),
            "google_id": idinfo.get("sub", ""),
        }
    except ValueError as e:
        logger.error("Google token verification failed: %s", e)
        return None


# ── Email OTP Delivery ──────────────────────────────────────
async def send_otp_email(email: str, otp: str, name: str = "") -> bool:
    """Send OTP code to user's email via SMTP."""
    try:
        import aiosmtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        if not SMTP_HOST or not SMTP_USER:
            # Fallback: log OTP to console in dev mode
            logger.warning(
                "SMTP not configured. OTP for %s: %s (dev mode)", email, otp
            )
            return True

        greeting = f"Hi {name}," if name else "Hi,"

        html_body = f"""
        <div style="font-family: 'Inter', -apple-system, sans-serif; max-width: 480px; margin: 0 auto; padding: 40px 24px; background: #f9f9fb;">
            <div style="background: white; border-radius: 16px; padding: 40px 32px; box-shadow: 0 4px 24px rgba(0,0,0,0.06);">
                <div style="text-align: center; margin-bottom: 32px;">
                    <h1 style="font-size: 20px; font-weight: 700; color: #1a1c1d; margin: 0;">DataDNA AI</h1>
                    <p style="font-size: 13px; color: #727784; margin-top: 4px;">Secure Verification</p>
                </div>
                <p style="font-size: 15px; color: #1a1c1d;">{greeting}</p>
                <p style="font-size: 15px; color: #414753;">Your one-time verification code is:</p>
                <div style="text-align: center; margin: 24px 0;">
                    <span style="font-size: 36px; font-weight: 800; letter-spacing: 8px; color: #004e9f; background: #d7e3ff; padding: 16px 32px; border-radius: 12px; display: inline-block;">{otp}</span>
                </div>
                <p style="font-size: 13px; color: #727784; text-align: center;">This code expires in <strong>5 minutes</strong>.</p>
                <hr style="border: none; border-top: 1px solid #e2e2e4; margin: 24px 0;" />
                <p style="font-size: 12px; color: #727784; text-align: center;">If you didn't request this, please ignore this email.</p>
            </div>
        </div>
        """

        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"DataDNA AI — Your Verification Code: {otp}"
        msg["From"] = SMTP_USER
        msg["To"] = email
        msg.attach(MIMEText(f"Your DataDNA AI verification code is: {otp}\nExpires in 5 minutes.", "plain"))
        msg.attach(MIMEText(html_body, "html"))

        await aiosmtplib.send(
            msg,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            username=SMTP_USER,
            password=SMTP_PASS,
            use_tls=False,
            start_tls=True,
        )
        logger.info("OTP email sent to %s", email)
        return True

    except Exception as e:
        logger.error("Failed to send OTP email to %s: %s", email, e)
        # In dev mode, log OTP to console so testing is possible
        logger.warning("DEV FALLBACK — OTP for %s: %s", email, otp)
        return True
