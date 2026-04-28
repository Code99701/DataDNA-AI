"""
Verification service — orchestrates the full document verification pipeline.

Tiered matching strategy:
  1. Exact file-level hash match → immediate result
  2. Exact page-level hash match → 100% similarity
  3. DL embedding similarity → scored match
  4. Chunk-level analysis → for moderate matches (0.7–0.85)

Aggregates results with multi-owner attribution and contribution percentages.
"""
import logging
from collections import defaultdict
from typing import List, Dict, Any, Optional

import numpy as np
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from app.config import SIMILARITY_THRESHOLD, CHUNK_ANALYSIS_LOW, CHUNK_ANALYSIS_HIGH

from app.services.document_hasher import hash_file, hash_text
from app.services.text_extractor import extract_text_by_pages
from app.services.embedding_service import EmbeddingService

logger = logging.getLogger(__name__)


async def verify_document(
    file_path: str,
    filename: str,
    file_ext: str,
    db: AsyncIOMotorDatabase,
) -> dict:
    """
    Verify a document against all registered documents.

    Implements tiered matching: file hash → page hash → embedding similarity
    → chunk-level analysis.

    Args:
        file_path: Path to the uploaded file on disk.
        filename: Original filename.
        file_ext: File extension (pdf, docx, txt).
        db: SQLAlchemy database session.

    Returns:
        Structured verification report with ownership and similarity data.
    """
    # ──────────────────────────────────────────────
    # Step 1: File-level hash check
    # ──────────────────────────────────────────────
    logger.info(f"Step 1: File-level hash check — {filename}")
    file_hash_value = hash_file(file_path)

    exact_match = await db.documents.find_one({"file_hash": file_hash_value})

    if exact_match:
        logger.info(f"Exact file match found — owner: {exact_match['owner_name']}")
        return {
            "status": "exact_match",
            "message": "Exact file match found. This file is already registered.",
            "file_hash": file_hash_value,
            "overall_similarity": 100.0,
            "dominant_owner": {
                "owner_id": exact_match['owner_id'],
                "owner_name": exact_match['owner_name'],
                "matched_documents": [exact_match.get("filename", "Unknown")],
                "contribution": 100.0,
                "pages_matched": exact_match.get("total_pages", 1),
                "avg_similarity": 100.0,
            },
            "owners": [
                {
                    "owner_id": exact_match['owner_id'],
                    "owner_name": exact_match['owner_name'],
                    "matched_documents": [exact_match.get("filename", "Unknown")],
                    "contribution": 100.0,
                    "pages_matched": exact_match.get("total_pages", 1),
                    "avg_similarity": 100.0,
                }
            ],
            "matched_pages": [],
            "chunk_analysis": [],
            "unmatched_pages": [],
            "total_pages_analyzed": 0,
        }

    # ──────────────────────────────────────────────
    # Step 2: Extract pages from target file
    # ──────────────────────────────────────────────
    logger.info("Step 2: Extracting pages from target file")
    target_pages = extract_text_by_pages(file_path, file_ext)
    total_pages = len(target_pages)
    logger.info(f"Target file has {total_pages} pages")

    # ──────────────────────────────────────────────
    # Step 3: Load all stored pages from DB
    # ──────────────────────────────────────────────
    logger.info("Step 3: Loading stored pages from database")
    all_stored_pages = await db.document_pages.find().to_list(length=None)

    if not all_stored_pages:
        logger.info("No documents registered in the system yet")
        return {
            "status": "no_match",
            "message": "No registered documents found in the system.",
            "file_hash": file_hash_value,
            "overall_similarity": 0.0,
            "dominant_owner": None,
            "owners": [],
            "matched_pages": [],
            "chunk_analysis": [],
            "unmatched_pages": list(range(1, total_pages + 1)),
            "total_pages_analyzed": total_pages,
        }

    # Pre-load stored embeddings and build lookup structures
    stored_page_hashes: Dict[str, List[dict]] = defaultdict(list)
    stored_embeddings_list = []
    stored_pages_with_embeddings = []

    for sp in all_stored_pages:
        stored_page_hashes[sp['page_hash']].append(sp)
        if sp['embedding'] is not None:
            emb = EmbeddingService.deserialize_embedding(sp['embedding'])
            stored_embeddings_list.append(emb)
            stored_pages_with_embeddings.append(sp)

    stored_embeddings_matrix = (
        np.vstack(stored_embeddings_list) if stored_embeddings_list else None
    )

    # Pre-build owner_id lookup for stored pages with embeddings
    doc_cache = {}

    async def get_doc(doc_id: str):
        if doc_id not in doc_cache:
            doc_cache[doc_id] = await db.documents.find_one({"_id": ObjectId(doc_id)})
        return doc_cache[doc_id]

    stored_page_owner_ids = []
    for sp in stored_pages_with_embeddings:
        doc = await get_doc(sp['document_id'])
        stored_page_owner_ids.append(doc['owner_id'] if doc else None)

    # ──────────────────────────────────────────────
    # Step 4: Page-level matching (best match PER OWNER)
    # ──────────────────────────────────────────────
    logger.info("Step 4: Page-level matching (per-owner)")

    matched_pages = []
    chunk_analysis = []
    unmatched_pages = []

    for page_idx, page_text in enumerate(target_pages):
        page_num = page_idx + 1
        page_hash_value = hash_text(page_text)
        page_had_match = False

        # ── Case A: Exact page hash match — record for ALL owners ──
        if page_hash_value in stored_page_hashes:
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
                    logger.info(
                        f"  Page {page_num}: exact hash match -> {doc['owner_name']} "
                        f"page {sp['page_number']}"
                    )
            if page_had_match:
                continue

        # ── Case B: DL embedding similarity — best match PER OWNER ──
        if stored_embeddings_matrix is not None:
            page_embedding = EmbeddingService.generate_embedding(page_text)
            similarities = EmbeddingService.compute_similarity_matrix(
                page_embedding.reshape(1, -1), stored_embeddings_matrix
            )[0]

            # Group by owner_id, keep best score per owner
            best_per_owner: Dict[str, tuple] = {}
            for s_idx, score in enumerate(similarities):
                oid = stored_page_owner_ids[s_idx]
                if oid is None:
                    continue
                score_f = float(score)
                if oid not in best_per_owner or score_f > best_per_owner[oid][0]:
                    best_per_owner[oid] = (score_f, s_idx)

            # Record matches for each owner above threshold
            for oid, (best_score, best_s_idx) in best_per_owner.items():
                best_stored = stored_pages_with_embeddings[best_s_idx]
                doc = await get_doc(best_stored['document_id'])
                if not doc:
                    continue

                if best_score >= SIMILARITY_THRESHOLD:
                    matched_pages.append({
                        "target_page": page_num,
                        "matched_page": best_stored['page_number'],
                        "matched_document": doc['filename'],
                        "owner_id": doc['owner_id'],
                        "owner_name": doc['owner_name'],
                        "similarity": round(best_score * 100, 2),
                        "match_type": "embedding",
                    })
                    page_had_match = True
                    logger.info(
                        f"  Page {page_num}: embedding match -> {doc['owner_name']} "
                        f"page {best_stored['page_number']} ({best_score:.3f})"
                    )

                    # Chunk-level analysis for moderate matches
                    if CHUNK_ANALYSIS_LOW <= best_score <= CHUNK_ANALYSIS_HIGH:
                        chunk_result = await _analyze_chunks(
                            page_num, page_text, best_stored, doc, db
                        )
                        if chunk_result:
                            chunk_analysis.append(chunk_result)

                elif best_score >= CHUNK_ANALYSIS_LOW:
                    chunk_result = await _analyze_chunks(
                        page_num, page_text, best_stored, doc, db
                    )
                    if chunk_result and chunk_result["chunks"]:
                        chunk_analysis.append(chunk_result)
                        matched_pages.append({
                            "target_page": page_num,
                            "matched_page": best_stored['page_number'],
                            "matched_document": doc['filename'],
                            "owner_id": doc['owner_id'],
                            "owner_name": doc['owner_name'],
                            "similarity": round(best_score * 100, 2),
                            "match_type": "chunk_analysis",
                        })
                        page_had_match = True
                        logger.info(
                            f"  Page {page_num}: chunk-level match -> {doc['owner_name']} "
                            f"({best_score:.3f})"
                        )

        if not page_had_match:
            unmatched_pages.append(page_num)
            logger.info(f"  Page {page_num}: no match found")

    # ──────────────────────────────────────────────
    # Step 5: Aggregate results
    # ──────────────────────────────────────────────
    logger.info("Step 5: Aggregating results")
    result = _aggregate_results(
        file_hash_value, matched_pages, chunk_analysis,
        unmatched_pages, total_pages
    )

    return result


async def _analyze_chunks(
    target_page_num: int,
    target_text: str,
    stored_page: dict,
    doc: dict,
    db: AsyncIOMotorDatabase,
) -> Optional[Dict[str, Any]]:
    """
    Perform chunk-level (paragraph) analysis for moderate similarity matches.

    Splits both the target page and the stored page into paragraphs,
    then compares each target paragraph against each stored paragraph.
    """
    logger.info(f"  Chunk-level analysis for page {target_page_num}")

    target_chunks = _split_into_chunks(target_text)
    stored_text = stored_page.get('page_text') or ""
    stored_chunks = _split_into_chunks(stored_text)

    if not target_chunks or not stored_chunks:
        return None

    # Generate embeddings for all chunks
    target_embeddings = EmbeddingService.generate_embeddings_batch(target_chunks)
    stored_embeddings = EmbeddingService.generate_embeddings_batch(stored_chunks)

    # Compare each target chunk against stored chunks
    sim_matrix = EmbeddingService.compute_similarity_matrix(
        target_embeddings, stored_embeddings
    )

    chunk_matches = []
    for i, row in enumerate(sim_matrix):
        best_j = int(np.argmax(row))
        best_sim = float(row[best_j])

        if best_sim >= CHUNK_ANALYSIS_LOW:
            chunk_matches.append({
                "paragraph": i + 1,
                "matched_paragraph": best_j + 1,
                "matched_owner": doc['owner_name'],
                "matched_owner_id": doc['owner_id'],
                "similarity": round(best_sim * 100, 2),
            })

    return {
        "target_page": target_page_num,
        "total_paragraphs": len(target_chunks),
        "matched_paragraphs": len(chunk_matches),
        "chunks": chunk_matches,
    }


def _split_into_chunks(text: str) -> List[str]:
    """
    Split text into paragraph-level chunks.

    Filters out very short paragraphs (< 30 chars) to avoid
    noise from headers, blank lines, etc.
    """
    paragraphs = text.split("\n")
    # Filter out trivially short paragraphs
    chunks = [p.strip() for p in paragraphs if len(p.strip()) >= 30]
    return chunks if chunks else [text]  # Fallback: use full text as one chunk


def _aggregate_results(
    file_hash: str,
    matched_pages: List[Dict],
    chunk_analysis: List[Dict],
    unmatched_pages: List[int],
    total_pages: int,
) -> dict:
    """
    Aggregate page-level matches into a final ownership report.

    Computes:
    - Dominant owner (highest contribution)
    - Per-owner contribution percentage
    - Overall similarity score
    """
    if not matched_pages:
        return {
            "status": "no_match",
            "message": "No matching content found in registered documents.",
            "file_hash": file_hash,
            "overall_similarity": 0.0,
            "dominant_owner": None,
            "owners": [],
            "matched_pages": [],
            "chunk_analysis": chunk_analysis,
            "unmatched_pages": unmatched_pages,
            "total_pages_analyzed": total_pages,
        }

    # ── Calculate per-owner contributions ──
    # Key: (owner_id, owner_name) composite — handles same user registering under
    # different owner_name strings (they appear as separate owners in the report)
    key_scores: Dict[tuple, dict] = defaultdict(lambda: {"total_similarity": 0.0, "pages": set()})
    key_docs: Dict[tuple, set] = defaultdict(set)

    for match in matched_pages:
        key = (match["owner_id"], match["owner_name"])
        key_scores[key]["total_similarity"] += match["similarity"]
        key_scores[key]["pages"].add(match["target_page"])
        key_docs[key].add(match["matched_document"])

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

    # Sort by contribution descending
    owners.sort(key=lambda x: x["contribution"], reverse=True)

    # Overall similarity: unique matched pages / total pages
    overall_sim = round(len(all_matched_page_nums) / total_pages * 100, 2) if total_pages > 0 else 0.0
    overall_sim = min(overall_sim, 100.0)

    # Determine status
    if len(owners) > 1:
        status = "multiple_owners"
        owner_names_str = ", ".join([o["owner_name"] for o in owners])
        message = f"This file has multiple owners. Content matches data from: {owner_names_str}."
    elif overall_sim >= 90:
        status = "high_match"
        message = "Very high similarity detected. Likely the same content."
    elif overall_sim >= 50:
        status = "partial_match"
        message = "Significant partial matches found across multiple pages."
    else:
        status = "low_match"
        message = "Some similar content detected but overall similarity is low."

    return {
        "status": status,
        "message": message,
        "file_hash": file_hash,
        "overall_similarity": overall_sim,
        "dominant_owner": owners[0] if owners else None,
        "owners": owners,
        "matched_pages": matched_pages,
        "chunk_analysis": chunk_analysis,
        "unmatched_pages": unmatched_pages,
        "total_pages_analyzed": total_pages,
    }
