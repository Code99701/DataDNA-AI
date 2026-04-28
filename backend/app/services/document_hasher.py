"""
Document hashing service using SHA-256.

Provides two levels of hashing:
- File-level: hash of raw file bytes (for exact duplicate detection)
- Text-level: hash of normalized text content (for page-level matching)
"""
import hashlib
import logging

logger = logging.getLogger(__name__)

CHUNK_SIZE = 8192  # Read files in 8KB chunks


def hash_file(file_path: str) -> str:
    """
    Generate SHA-256 hash of the raw file bytes.

    Reads in chunks for memory efficiency on large files.

    Args:
        file_path: Path to the file on disk.

    Returns:
        Hex string of the SHA-256 hash.
    """
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            sha256.update(chunk)

    file_hash = sha256.hexdigest()
    logger.info(f"File hash: {file_hash[:16]}...")
    return file_hash


def hash_text(text: str) -> str:
    """
    Generate SHA-256 hash of normalized text.

    Normalization: strip leading/trailing whitespace, collapse internal
    whitespace to single spaces, convert to lowercase. This ensures
    minor formatting differences don't produce different hashes.

    Args:
        text: Raw text content.

    Returns:
        Hex string of the SHA-256 hash.
    """
    # Normalize: strip, collapse whitespace, lowercase
    normalized = " ".join(text.split()).lower().strip()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()
