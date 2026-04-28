"""
Local blockchain for immutable file ownership tracking.

Each block records an (owner_name, file_hash) pair. Blocks are linked
via SHA-256 hashes to form a tamper-proof chain. The chain is persisted
to a JSON file so it survives server restarts.

Usage:
    from app.services.blockchain import blockchain
    block = blockchain.add_block("Alice", "abc123...")
    valid = blockchain.verify_chain()
"""
import hashlib
import json
import logging
import os
import threading
from datetime import datetime, timezone
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

BLOCKCHAIN_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "storage", "blockchain.json",
)


class Block:
    """A single block in the ownership blockchain."""

    def __init__(
        self,
        index: int,
        timestamp: str,
        owner_name: str,
        file_hash: str,
        previous_hash: str,
    ):
        self.index = index
        self.timestamp = timestamp
        self.owner_name = owner_name
        self.file_hash = file_hash
        self.previous_hash = previous_hash
        self.block_hash = self._calculate_hash()

    def _calculate_hash(self) -> str:
        """SHA-256 hash of all block fields (excluding block_hash itself)."""
        payload = (
            f"{self.index}"
            f"{self.timestamp}"
            f"{self.owner_name}"
            f"{self.file_hash}"
            f"{self.previous_hash}"
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def to_dict(self) -> dict:
        """Serialize block to a dictionary."""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "owner_name": self.owner_name,
            "file_hash": self.file_hash,
            "previous_hash": self.previous_hash,
            "block_hash": self.block_hash,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Block":
        """Deserialize a block from a dictionary."""
        block = cls(
            index=data["index"],
            timestamp=data["timestamp"],
            owner_name=data["owner_name"],
            file_hash=data["file_hash"],
            previous_hash=data["previous_hash"],
        )
        block.block_hash = data["block_hash"]
        return block


class Blockchain:
    """
    Thread-safe local blockchain for file ownership records.

    The chain is persisted to a JSON file and loaded on startup.
    A genesis block is created automatically if no chain file exists.
    """

    def __init__(self):
        self._lock = threading.Lock()
        self.chain: List[Block] = []
        self._load_chain()

    # ── Chain management ─────────────────────────────

    def _create_genesis_block(self) -> Block:
        """Create the first block in the chain."""
        return Block(
            index=0,
            timestamp=datetime.now(timezone.utc).isoformat(),
            owner_name="GENESIS",
            file_hash="0" * 64,
            previous_hash="0" * 64,
        )

    def add_block(self, owner_name: str, file_hash: str) -> Block:
        """
        Add a new ownership record to the blockchain.

        Args:
            owner_name: Name of the file owner.
            file_hash: SHA-256 hash of the file.

        Returns:
            The newly created Block.
        """
        with self._lock:
            previous_block = self.chain[-1]
            new_block = Block(
                index=len(self.chain),
                timestamp=datetime.now(timezone.utc).isoformat(),
                owner_name=owner_name,
                file_hash=file_hash,
                previous_hash=previous_block.block_hash,
            )
            self.chain.append(new_block)
            self._save_chain()
            logger.info(
                f"Block #{new_block.index} added — "
                f"owner={owner_name}, file_hash={file_hash[:16]}..."
            )
            return new_block

    def verify_chain(self) -> Dict:
        """
        Verify the integrity of the entire blockchain.

        Returns:
            Dict with 'valid' (bool), 'total_blocks', and 'errors' list.
        """
        with self._lock:
            errors = []

            for i in range(1, len(self.chain)):
                current = self.chain[i]
                previous = self.chain[i - 1]

                # Check hash linkage
                if current.previous_hash != previous.block_hash:
                    errors.append(
                        f"Block #{i}: previous_hash mismatch "
                        f"(expected {previous.block_hash[:16]}..., "
                        f"got {current.previous_hash[:16]}...)"
                    )

                # Check block's own hash integrity
                recalculated = current._calculate_hash()
                if current.block_hash != recalculated:
                    errors.append(
                        f"Block #{i}: block_hash corrupted "
                        f"(expected {recalculated[:16]}..., "
                        f"got {current.block_hash[:16]}...)"
                    )

            return {
                "valid": len(errors) == 0,
                "total_blocks": len(self.chain),
                "errors": errors,
            }

    def get_block_by_file_hash(self, file_hash: str) -> Optional[Block]:
        """Look up a block by the file hash it records."""
        with self._lock:
            for block in reversed(self.chain):
                if block.file_hash == file_hash:
                    return block
            return None

    def get_blocks_by_owner(self, owner_name: str) -> List[Block]:
        """Get all blocks belonging to a specific owner."""
        with self._lock:
            return [
                b for b in self.chain
                if b.owner_name.lower() == owner_name.lower()
                and b.index > 0  # skip genesis
            ]

    def get_chain(self) -> List[dict]:
        """Return the full chain as a list of dicts."""
        with self._lock:
            return [block.to_dict() for block in self.chain]

    # ── Persistence ──────────────────────────────────

    def _save_chain(self):
        """Persist the chain to a JSON file."""
        os.makedirs(os.path.dirname(BLOCKCHAIN_FILE), exist_ok=True)
        data = [block.to_dict() for block in self.chain]
        with open(BLOCKCHAIN_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _load_chain(self):
        """Load the chain from the JSON file, or create genesis."""
        if os.path.exists(BLOCKCHAIN_FILE):
            try:
                with open(BLOCKCHAIN_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.chain = [Block.from_dict(d) for d in data]
                logger.info(
                    f"Blockchain loaded — {len(self.chain)} blocks"
                )
                return
            except (json.JSONDecodeError, KeyError) as e:
                logger.warning(
                    f"Corrupted blockchain file, reinitializing: {e}"
                )

        # Create fresh chain with genesis block
        self.chain = [self._create_genesis_block()]
        self._save_chain()
        logger.info("Blockchain initialized with genesis block")


# ── Module-level singleton ───────────────────────────
blockchain = Blockchain()
