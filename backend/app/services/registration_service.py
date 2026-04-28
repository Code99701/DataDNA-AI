"""
Registration service — orchestrates the full file registration pipeline.

Flow:
  1. Hash the file → check for exact duplicates
  2. Extract text pages
  3. For each page: generate hash + DL embedding
  4. Pre-flight similarity check against already-registered documents.
     If significant overlap found (>= REGISTRATION_SIMILARITY_BLOCK_THRESHOLD),
     return a similarity report instead of registering a new entry.
  5. Store everything in the database
  6. Record on blockchain
"""
import os
import logging
from collections import defaultdict
from datetime import datetime, timezone
from typing import List, Dict

import numpy as np
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from app.config import (
    REGISTRATION_SIMILARITY_BLOCK_THRESHOLD,
    SIMILARITY_THRESHOLD,
    CHUNK_ANALYSIS_LOW,
)


from app.services.document_hasher import hash_file, hash_text
from app.services.text_extractor import extract_text_by_pages
from app.services.embedding_service import EmbeddingService
from app.services.blockchain import blockchain

logger = logging.getLogger(__name__)


async def _compute_similarity_breakdown(
    target_pages: List[str],
    db: AsyncIOMotorDatabase,
) -> dict:
    """
    Compare each page of a new file against all stored page embeddings.

    Returns a dict with:
      - overall_similarity  : float (0–100)
      - owners              : list of {owner_id, owner_name, contribution, pages_matched, avg_similarity}
      - matched_pages       : list of per-page match details
      - unmatched_pages     : list of page numbers with no match
    """
    total_pages = len(target_pages)

    # Load all stored pages
    all_stored = await db.document_pages.find().to_list(length=None)
    if not all_stored:
        return {
            "overall_similarity": 0.0,
            "owners": [],
            "matched_pages": [],
            "unmatched_pages": list(range(1, total_pages + 1)),
            "total_pages": total_pages,
        }

    # Build hash lookup and embedding matrix
    # Also build a mapping from stored page → owner_id for per-owner grouping
    stored_page_hashes: Dict[str, List[dict]] = defaultdict(list)
    stored_embeddings_list = []
    stored_pages_with_embeddings = []

    for sp in all_stored:
        stored_page_hashes[sp['page_hash']].append(sp)
        if sp['embedding'] is not None:
            emb = EmbeddingService.deserialize_embedding(sp['embedding'])
            stored_embeddings_list.append(emb)
            stored_pages_with_embeddings.append(sp)

    stored_matrix = (
        np.vstack(stored_embeddings_list) if stored_embeddings_list else None
    )

    matched_pages = []
    unmatched_pages = []

    # Cache doc lookups to avoid N+1 queries
    doc_cache = {}

    async def get_doc(doc_id: str):
        if doc_id not in doc_cache:
            doc_cache[doc_id] = await db.documents.find_one({"_id": ObjectId(doc_id)})
        return doc_cache[doc_id]

    # Pre-build owner_id lookup for stored pages with embeddings
    # so we can find best match PER OWNER (not just global best)
    stored_page_owner_ids = []
    for sp in stored_pages_with_embeddings:
        doc = await get_doc(sp['document_id'])
        stored_page_owner_ids.append(doc['owner_id'] if doc else None)

    # Batch-generate embeddings for all target pages at once
    target_embeddings = (
        EmbeddingService.generate_embeddings_batch(target_pages)
        if stored_matrix is not None
        else None
    )

    for page_idx, page_text in enumerate(target_pages):
        page_num = page_idx + 1
        page_hash_value = hash_text(page_text)
        page_had_match = False

        # ── Case A: Exact page hash match ──
        if page_hash_value in stored_page_hashes:
            # Record matches for ALL owners that have this exact page
            seen_owners = set()
            for sp in stored_page_hashes[page_hash_value]:
                doc = await get_doc(sp['document_id'])
                if doc and doc['owner_id'] not in seen_owners:
                    seen_owners.add(doc['owner_id'])
                    matched_pages.append({
                        "target_page": page_num,
                        "matched_page": sp['page_number'],
                        "matched_document": doc['filename'],
                        "owner_id": doc['owner_id'],
                        "owner_name": doc['owner_name'],
                        "similarity": 100.0,
                        "match_type": "exact_hash",
                    })
                    page_had_match = True
            if page_had_match:
                continue

        # ── Case B: Embedding similarity — find best match PER OWNER ──
        if stored_matrix is not None and target_embeddings is not None:
            page_emb = target_embeddings[page_idx].reshape(1, -1)
            sims = EmbeddingService.compute_similarity_matrix(page_emb, stored_matrix)[0]

            # Group similarities by owner_id, keep the best score per owner
            best_per_owner: Dict[str, tuple] = {}  # owner_id -> (score, stored_page_idx)
            for s_idx, score in enumerate(sims):
                oid = stored_page_owner_ids[s_idx]
                if oid is None:
                    continue
                score_f = float(score)
                if oid not in best_per_owner or score_f > best_per_owner[oid][0]:
                    best_per_owner[oid] = (score_f, s_idx)

            # Record a match for each owner that exceeds the threshold
            for oid, (best_score, best_s_idx) in best_per_owner.items():
                if best_score >= SIMILARITY_THRESHOLD:
                    sp = stored_pages_with_embeddings[best_s_idx]
                    doc = await get_doc(sp['document_id'])
                    if doc:
                        matched_pages.append({
                            "target_page": page_num,
                            "matched_page": sp['page_number'],
                            "matched_document": doc['filename'],
                            "owner_id": doc['owner_id'],
                            "owner_name": doc['owner_name'],
                            "similarity": round(best_score * 100, 2),
                            "match_type": "embedding",
                        })
                        page_had_match = True
                elif best_score >= CHUNK_ANALYSIS_LOW:
                    sp = stored_pages_with_embeddings[best_s_idx]
                    doc = await get_doc(sp['document_id'])
                    if doc:
                        matched_pages.append({
                            "target_page": page_num,
                            "matched_page": sp['page_number'],
                            "matched_document": doc['filename'],
                            "owner_id": doc['owner_id'],
                            "owner_name": doc['owner_name'],
                            "similarity": round(best_score * 100, 2),
                            "match_type": "partial_embedding",
                        })
                        page_had_match = True

        if not page_had_match:
            unmatched_pages.append(page_num)

    # ── Aggregate per-owner contributions ──
    # Key: (owner_id, owner_name) composite — handles same user registering under
    # different owner_name strings (they appear as separate owners in the report)
    key_scores: Dict[tuple, dict] = defaultdict(lambda: {"total_similarity": 0.0, "pages": set()})
    key_docs: Dict[tuple, set] = defaultdict(set)

    for m in matched_pages:
        key = (m["owner_id"], m["owner_name"])
        key_scores[key]["total_similarity"] += m["similarity"]
        key_scores[key]["pages"].add(m["target_page"])
        key_docs[key].add(m["matched_document"])

    # Contribution = absolute % of uploaded file's pages that match this owner
    # (not relative to other owners — so both can show 50% for a 50/50 merged file)
    owners = []
    all_matched_page_nums: set = set()
    for key, data in key_scores.items():
        oid, oname = key
        pages_matched = len(data["pages"])
        all_matched_page_nums |= data["pages"]
        contribution = round((pages_matched / total_pages) * 100, 2) if total_pages > 0 else 0.0
        docs_list = sorted(key_docs[key])
        owners.append({
            "owner_id": oid,
            "owner_name": oname,
            "matched_documents": docs_list,
            "contribution": contribution,
            "pages_matched": pages_matched,
            "avg_similarity": round(data["total_similarity"] / pages_matched, 2) if pages_matched > 0 else 0.0,
        })

    owners.sort(key=lambda x: x["contribution"], reverse=True)

    # Overall similarity: unique matched pages / total pages
    overall_sim = round(len(all_matched_page_nums) / total_pages * 100, 2) if total_pages > 0 else 0.0
    overall_sim = min(overall_sim, 100.0)

    return {
        "overall_similarity": overall_sim,
        "owners": owners,
        "matched_pages": matched_pages,
        "unmatched_pages": unmatched_pages,
        "total_pages": total_pages,
    }


async def register_document(
    file_path: str,
    filename: str,
    file_ext: str,
    owner_id: str,
    owner_name: str,
    db: AsyncIOMotorDatabase,
) -> dict:
    """
    Register a document for ownership tracking.

    Args:
        file_path: Path to the uploaded file on disk.
        filename: Original filename.
        file_ext: File extension (pdf, docx, txt).
        owner_id: Unique identifier for the owner.
        owner_name: Human-readable owner name.
        db: SQLAlchemy database session.

    Returns:
        Dictionary with registration result.
    """
    # ──────────────────────────────────────────────
    # Step 1: File-level hash — exact duplicate check
    # ──────────────────────────────────────────────
    logger.info(f"Step 1: Hashing file — {filename}")
    file_hash_value = hash_file(file_path)

    existing = await db.documents.find_one({"file_hash": file_hash_value})

    if existing:
        logger.info(f"File already registered by {existing['owner_name']}")
        return {
            "status": "already_registered",
            "message": "This exact file has already been registered.",
            "file_hash": file_hash_value,
            "existing_owner": {
                "owner_id": existing['owner_id'],
                "owner_name": existing['owner_name'],
                "registered_at": existing['registered_at'].isoformat(),
            },
        }

    # ──────────────────────────────────────────────
    # Step 2: Extract pages
    # ──────────────────────────────────────────────
    logger.info("Step 2: Extracting text pages")
    pages = extract_text_by_pages(file_path, file_ext)
    total_pages = len(pages)
    logger.info(f"Extracted {total_pages} pages")

    # ──────────────────────────────────────────────
    # Step 3: Pre-flight similarity check
    # Compare against all already-registered documents.
    # If significant similarity is found, block registration
    # and return a similarity breakdown report.
    # ──────────────────────────────────────────────
    logger.info("Step 3: Pre-flight similarity check against registered documents")
    similarity_report = await _compute_similarity_breakdown(pages, db)

    block_threshold_pct = REGISTRATION_SIMILARITY_BLOCK_THRESHOLD * 100
    if similarity_report["overall_similarity"] >= block_threshold_pct:
        logger.info(
            f"Similarity check blocked registration — "
            f"overall similarity: {similarity_report['overall_similarity']}%"
        )

        owners = similarity_report["owners"]
        matched_pages = similarity_report["matched_pages"]
        
        # Build a detailed breakdown of top matches
        match_examples = []
        for m in matched_pages[:5]: # Show top 5 matches
            doc_name = m["matched_document"]
            match_examples.append(
                f"Page {m['target_page']} matches {m['owner_name']}'s \"{doc_name}\" Page {m['matched_page']} ({m['similarity']}%)"
            )
        
        examples_str = "\n".join(match_examples)
        if len(matched_pages) > 5:
            examples_str += f"\n... and {len(matched_pages) - 5} more matches."

        if len(owners) > 1:
            owner_breakdown = ", ".join(
                f"{o['owner_name']} ({o['contribution']}%)" for o in owners
            )
            message = (
                f"This file appears to be derived from multiple registered documents.\n"
                f"Content attribution: {owner_breakdown}.\n\n"
                f"Top Matches:\n{examples_str}\n\n"
                f"Registration blocked to preserve original ownership records."
            )
        elif len(owners) == 1:
            o = owners[0]
            message = (
                f"This file is {o['contribution']}% similar to a document already "
                f"registered by {o['owner_name']}.\n\n"
                f"Top Matches:\n{examples_str}\n\n"
                f"Registration blocked to preserve original ownership."
            )
        else:
            message = "High similarity detected with registered documents."

        return {
            "status": "similarity_detected",
            "message": message,
            "file_hash": file_hash_value,
            "filename": filename,
            "overall_similarity": similarity_report["overall_similarity"],
            "dominant_owner": owners[0] if owners else None,
            "owners": owners,
            "matched_pages": similarity_report["matched_pages"],
            "unmatched_pages": similarity_report["unmatched_pages"],
            "total_pages_analyzed": total_pages,
        }

    logger.info(
        f"Similarity check passed — "
        f"overall similarity: {similarity_report['overall_similarity']}% "
        f"(threshold: {block_threshold_pct}%)"
    )

    # ──────────────────────────────────────────────
    # Step 4: Page-level processing (hash + embedding)
    # ──────────────────────────────────────────────
    logger.info("Step 4: Generating page hashes and embeddings")
    page_embeddings = EmbeddingService.generate_embeddings_batch(pages)

    # ──────────────────────────────────────────────
    # Step 5: Store in database
    # ──────────────────────────────────────────────
    logger.info("Step 5: Storing in database")

    doc = {
        "file_hash": file_hash_value,
        "filename": filename,
        "owner_id": owner_id,
        "owner_name": owner_name,
        "total_pages": total_pages,
        "registered_at": datetime.now(timezone.utc)
    }
    res = await db.documents.insert_one(doc)
    doc_id = str(res.inserted_id)

    page_records = []
    for i, (page_text, embedding) in enumerate(zip(pages, page_embeddings)):
        page_hash_value = hash_text(page_text)

        page_record = {
            "document_id": doc_id,
            "page_number": i + 1,
            "page_hash": page_hash_value,
            "embedding": EmbeddingService.serialize_embedding(embedding),
            "page_text": page_text
        }
        await db.document_pages.insert_one(page_record)
        page_records.append({
            "page_number": i + 1,
            "page_hash": page_hash_value,
        })


    logger.info(f"Registration complete — {total_pages} pages stored")

    # ──────────────────────────────────────────────
    # Step 6: Record on blockchain
    # ──────────────────────────────────────────────
    logger.info("Step 6: Recording ownership on blockchain")
    block = blockchain.add_block(owner_name=owner_name, file_hash=file_hash_value)

    db_block = {
        "block_index": block.index,
        "block_hash": block.block_hash,
        "previous_hash": block.previous_hash,
        "file_hash": block.file_hash,
        "owner_name": block.owner_name,
        "timestamp": datetime.fromisoformat(block.timestamp),
    }
    await db.blockchain_blocks.insert_one(db_block)

    logger.info(f"Blockchain block #{block.index} recorded")

    return {
        "status": "registered",
        "file_hash": file_hash_value,
        "filename": filename,
        "owner_id": owner_id,
        "owner_name": owner_name,
        "total_pages": total_pages,
        "pages": page_records,
        "registered_at": doc['registered_at'].isoformat(),
        "blockchain": {
            "block_index": block.index,
            "block_hash": block.block_hash,
            "previous_hash": block.previous_hash,
            "timestamp": block.timestamp,
        },
    }
