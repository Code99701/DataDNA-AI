"""File storage service with Google Cloud Storage + local fallback."""

import logging
import os
import uuid

from app.core.config import GCP_PROJECT_ID, GCS_BUCKET_NAME, STORAGE_DIR

logger = logging.getLogger(__name__)

try:
    from google.cloud import storage as gcs_storage
except Exception:  # pragma: no cover - optional dependency at runtime
    gcs_storage = None


def _ensure_storage_dir():
    """Create the storage directory if it doesn't exist."""
    os.makedirs(STORAGE_DIR, exist_ok=True)


def _save_file_local(filename: str, content: bytes) -> tuple[str, str, str]:
    """Persist file to local disk."""
    _ensure_storage_dir()

    file_id = str(uuid.uuid4())
    _, ext = os.path.splitext(filename)
    stored_name = f"{file_id}{ext}"
    full_path = os.path.join(STORAGE_DIR, stored_name)

    with open(full_path, "wb") as f:
        f.write(content)

    logger.info("Saved file %s → %s (%d bytes) [local]", filename, stored_name, len(content))
    return file_id, stored_name, "local"


def _save_file_gcs(filename: str, content: bytes) -> tuple[str, str, str]:
    """Persist file to Google Cloud Storage."""
    if gcs_storage is None:
        raise RuntimeError("google-cloud-storage is not installed")
    if not GCS_BUCKET_NAME:
        raise RuntimeError("GCS_BUCKET_NAME is not configured")

    file_id = str(uuid.uuid4())
    _, ext = os.path.splitext(filename)
    object_name = f"uploads/{file_id}{ext}"

    client_kwargs = {}
    if GCP_PROJECT_ID:
        client_kwargs["project"] = GCP_PROJECT_ID
    client = gcs_storage.Client(**client_kwargs)
    bucket = client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(object_name)
    blob.upload_from_string(content)

    gcs_uri = f"gs://{GCS_BUCKET_NAME}/{object_name}"
    logger.info("Saved file %s → %s (%d bytes) [gcs]", filename, gcs_uri, len(content))
    return file_id, gcs_uri, "gcs"


def save_file(filename: str, content: bytes) -> tuple[str, str, str]:
    """
    Save file content with a unique name.

    Args:
        filename: Original filename from the upload.
        content:  Raw file bytes.

    Returns:
        Tuple of (file_id, location, storage_provider).
    """
    if GCS_BUCKET_NAME:
        try:
            return _save_file_gcs(filename, content)
        except Exception as exc:
            logger.warning("Falling back to local storage because GCS failed: %s", exc)

    return _save_file_local(filename, content)
