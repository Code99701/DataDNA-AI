"""
Admin API routes — user management, role assignment, dashboard access control.
Only accessible by users with role=admin and 2FA verified.
"""

import logging
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Depends

from app.database.database import get_db
from app.models.auth_models import (
    UpdateRoleRequest,
    UpdateAccessRequest,
    UserListItem,
    ActivityLogEntry,
    UserRole,
)
from app.api.dependencies import require_admin

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["Admin"])


async def _log_activity(db, action: str, admin_email: str, target_email: str = "", details: str = ""):
    """Record admin action in the activity_log collection."""
    entry = {
        "action": action,
        "admin_email": admin_email,
        "target_email": target_email,
        "details": details,
        "timestamp": datetime.now(timezone.utc),
    }
    await db.activity_log.insert_one(entry)


# ── GET /admin/users ─────────────────────────────────────────
@router.get("/users")
async def list_users(admin: dict = Depends(require_admin)):
    """List all users in the system."""
    db = get_db()
    cursor = db.users.find(
        {},
        {
            "_id": 0,
            "password_hash": 0,
            "otp_code": 0,
            "otp_expiry": 0,
            "trusted_devices": 0,
        },
    ).sort("created_at", -1)

    users = await cursor.to_list(length=1000)
    return {"users": users, "total": len(users)}


# ── PUT /admin/users/{user_id}/role ──────────────────────────
@router.put("/users/{user_id}/role")
async def update_user_role(
    user_id: str,
    body: UpdateRoleRequest,
    admin: dict = Depends(require_admin),
):
    """Promote or demote a user's role."""
    db = get_db()

    target_user = await db.users.find_one({"user_id": user_id})
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Prevent admin from demoting themselves
    if target_user["user_id"] == admin["user_id"] and body.role == UserRole.USER:
        raise HTTPException(status_code=400, detail="Cannot demote yourself")

    await db.users.update_one(
        {"user_id": user_id},
        {"$set": {"role": body.role.value}},
    )

    await _log_activity(
        db,
        action="role_change",
        admin_email=admin["email"],
        target_email=target_user["email"],
        details=f"Role changed to {body.role.value}",
    )

    logger.info(
        "Admin %s changed role of %s to %s",
        admin["email"],
        target_user["email"],
        body.role.value,
    )
    return {"message": f"User role updated to {body.role.value}"}


# ── PUT /admin/users/{user_id}/access ────────────────────────
@router.put("/users/{user_id}/access")
async def update_dashboard_access(
    user_id: str,
    body: UpdateAccessRequest,
    admin: dict = Depends(require_admin),
):
    """Grant or revoke dashboard access for a user."""
    db = get_db()

    target_user = await db.users.find_one({"user_id": user_id})
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.users.update_one(
        {"user_id": user_id},
        {"$set": {"dashboard_access": body.dashboard_access}},
    )

    action_word = "granted" if body.dashboard_access else "revoked"
    await _log_activity(
        db,
        action=f"access_{action_word}",
        admin_email=admin["email"],
        target_email=target_user["email"],
        details=f"Dashboard access {action_word}",
    )

    logger.info(
        "Admin %s %s dashboard access for %s",
        admin["email"],
        action_word,
        target_user["email"],
    )
    return {"message": f"Dashboard access {action_word}"}


# ── DELETE /admin/users/{user_id} ────────────────────────────
@router.delete("/users/{user_id}")
async def delete_user(user_id: str, admin: dict = Depends(require_admin)):
    """Delete a user account."""
    db = get_db()

    target_user = await db.users.find_one({"user_id": user_id})
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Prevent admin from deleting themselves
    if target_user["user_id"] == admin["user_id"]:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")

    await db.users.delete_one({"user_id": user_id})

    await _log_activity(
        db,
        action="user_deleted",
        admin_email=admin["email"],
        target_email=target_user["email"],
        details="User account deleted",
    )

    logger.info("Admin %s deleted user %s", admin["email"], target_user["email"])
    return {"message": "User deleted"}


# ── GET /admin/activity-log ──────────────────────────────────
@router.get("/activity-log")
async def get_activity_log(admin: dict = Depends(require_admin)):
    """View admin activity log."""
    db = get_db()
    cursor = db.activity_log.find({}, {"_id": 0}).sort("timestamp", -1)
    logs = await cursor.to_list(length=100)
    return {"logs": logs, "total": len(logs)}
