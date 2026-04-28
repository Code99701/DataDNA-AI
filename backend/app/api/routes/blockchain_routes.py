"""
API routes for the blockchain-based file ownership ledger.

Endpoints:
  GET  /blockchain/chain              — View the full blockchain
  GET  /blockchain/verify             — Verify blockchain integrity
  GET  /blockchain/block/{file_hash}  — Look up a block by file hash
  GET  /blockchain/owner/{owner_name} — Look up blocks by owner name
"""
import logging

from fastapi import APIRouter, HTTPException, Depends
from app.api.dependencies import get_current_user
from app.models.auth_models import UserDocument

from app.services.blockchain import blockchain

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/blockchain", tags=["Blockchain"])


@router.get("/chain")
async def get_full_chain():
    """
    Return the complete blockchain.

    Each block contains: index, timestamp, owner_name, file_hash,
    previous_hash, and block_hash.
    """
    chain = blockchain.get_chain()
    return {
        "total_blocks": len(chain),
        "chain": chain,
    }


@router.get("/verify")
async def verify_blockchain():
    """
    Verify the integrity of the entire blockchain.

    Checks hash linkage between all blocks and recalculates each
    block's hash to detect tampering.
    """
    result = blockchain.verify_chain()
    return {
        "valid": result["valid"],
        "total_blocks": result["total_blocks"],
        "message": (
            "Blockchain integrity verified — no tampering detected."
            if result["valid"]
            else f"Blockchain integrity FAILED — {len(result['errors'])} error(s) found."
        ),
        "errors": result["errors"],
    }


@router.get("/block/{file_hash}")
async def get_block_by_file_hash(file_hash: str):
    """
    Look up the blockchain record for a specific file hash.

    Path Parameters:
        file_hash: The SHA-256 hash of the file.
    """
    block = blockchain.get_block_by_file_hash(file_hash)

    if not block:
        raise HTTPException(
            status_code=404,
            detail=f"No blockchain record found for file hash: {file_hash[:16]}...",
        )

    return {
        "found": True,
        "block": block.to_dict(),
    }


@router.get("/owner/{owner_name}")
async def get_blocks_by_owner(owner_name: str):
    """
    Look up all blockchain records for a specific owner.

    Path Parameters:
        owner_name: The name of the file owner.
    """
    blocks = blockchain.get_blocks_by_owner(owner_name)

    return {
        "owner_name": owner_name,
        "total_blocks": len(blocks),
        "blocks": [b.to_dict() for b in blocks],
    }
