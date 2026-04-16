"""
Simple blockchain (hash-chain) service.

Each uploaded file's fingerprint is recorded as a block in a chain.
The chain is persisted to a JSON file for durability across restarts.
"""

import hashlib
import json
import os
import logging
from datetime import datetime, timezone
from typing import Optional

from app.core.config import BLOCKCHAIN_FILE

logger = logging.getLogger(__name__)


class Block:
    """A single block in the hash chain."""

    def __init__(
        self,
        index: int,
        timestamp: str,
        file_hash: str,
        previous_hash: str,
    ):
        self.index = index
        self.timestamp = timestamp
        self.file_hash = file_hash
        self.previous_hash = previous_hash
        self.current_hash = self._compute_hash()

    def _compute_hash(self) -> str:
        block_string = f"{self.index}{self.timestamp}{self.file_hash}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "file_hash": self.file_hash,
            "previous_hash": self.previous_hash,
            "current_hash": self.current_hash,
        }


class Blockchain:
    """In-memory hash-chain backed by a JSON file on disk."""

    def __init__(self, filepath: str = BLOCKCHAIN_FILE):
        self.filepath = filepath
        self.chain: list[Block] = []
        self._load_or_create()

    # ── Public API ──────────────────────────────────────────

    def add_block(self, file_hash: str) -> Block:
        """Append a new block for the given file hash and persist."""
        previous_hash = self.chain[-1].current_hash if self.chain else "0"
        block = Block(
            index=len(self.chain),
            timestamp=datetime.now(timezone.utc).isoformat(),
            file_hash=file_hash,
            previous_hash=previous_hash,
        )
        self.chain.append(block)
        self._save()
        logger.info("Blockchain block #%d added for hash %s", block.index, file_hash)
        return block

    def verify_chain(self) -> bool:
        """Validate the integrity of the entire chain."""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.previous_hash != previous.current_hash:
                logger.warning("Chain broken at block #%d", i)
                return False
            if current.current_hash != current._compute_hash():
                logger.warning("Block #%d hash mismatch", i)
                return False
        return True

    def get_chain(self) -> list[dict]:
        """Return the full chain as a list of dicts."""
        return [b.to_dict() for b in self.chain]

    def find_by_hash(self, file_hash: str) -> Optional[dict]:
        """Search the chain for a block containing the given file hash."""
        for block in self.chain:
            if block.file_hash == file_hash:
                return block.to_dict()
        return None

    # ── Persistence ─────────────────────────────────────────

    def _save(self):
        with open(self.filepath, "w") as f:
            json.dump([b.to_dict() for b in self.chain], f, indent=2)

    def _load_or_create(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                data = json.load(f)
            for item in data:
                block = Block(
                    index=item["index"],
                    timestamp=item["timestamp"],
                    file_hash=item["file_hash"],
                    previous_hash=item["previous_hash"],
                )
                # Restore the saved hash (it should match)
                block.current_hash = item["current_hash"]
                self.chain.append(block)
            logger.info("Loaded blockchain with %d blocks from %s", len(self.chain), self.filepath)
        else:
            logger.info("No existing blockchain found — starting fresh.")


# Module-level singleton
blockchain = Blockchain()
