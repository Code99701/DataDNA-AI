"""
File storage service — saves uploaded files to the local filesystem.
"""

import os
import logging
import uuid
from app.core.config import STORAGE_DIR

logger = logging.getLogger(__name__)


def _ensure_storage_dir():
    """Create the storage directory if it doesn't exist."""
    os.makedirs(STORAGE_DIR, exist_ok=True)


def save_file(filename: str, content: bytes) -> tuple[str, str]:
    """
    Save file content to disk with a unique name to avoid collisions.

    Args:
        filename: Original filename from the upload.
        content:  Raw file bytes.

    Returns:
        Tuple of (file_id, relative_path) where relative_path is
        relative to the storage root.
    """
    _ensure_storage_dir()

    file_id = str(uuid.uuid4())
    # Preserve original extension
    _, ext = os.path.splitext(filename)
    stored_name = f"{file_id}{ext}"
    full_path = os.path.join(STORAGE_DIR, stored_name)

    with open(full_path, "wb") as f:
        f.write(content)

    logger.info("Saved file %s → %s (%d bytes)", filename, stored_name, len(content))
    return file_id, stored_name
