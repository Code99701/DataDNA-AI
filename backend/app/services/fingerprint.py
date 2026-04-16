"""
Fingerprinting service — generates a SHA-256 hash of file contents.
"""

import hashlib
import logging

logger = logging.getLogger(__name__)

CHUNK_SIZE = 8192  # Read in 8 KB chunks to handle large files efficiently


def generate_fingerprint(file_bytes: bytes) -> str:
    """
    Generate a SHA-256 fingerprint from raw file bytes.

    Args:
        file_bytes: The complete file content as bytes.

    Returns:
        Hex-encoded SHA-256 hash string.
    """
    sha256 = hashlib.sha256()
    # Process in chunks to support streaming in the future
    offset = 0
    while offset < len(file_bytes):
        sha256.update(file_bytes[offset : offset + CHUNK_SIZE])
        offset += CHUNK_SIZE
    fingerprint = sha256.hexdigest()
    logger.debug("Generated fingerprint: %s", fingerprint)
    return fingerprint