import os

# Paths
BASE_DIR = r"d:\google solutions\Google-Solutions-2026-Project\backend_final\app"
REG_SERVICE = os.path.join(BASE_DIR, "services", "registration_service.py")
VER_SERVICE = os.path.join(BASE_DIR, "services", "verification_service.py")
OWNERSHIP_ROUTE = os.path.join(BASE_DIR, "api", "routes", "ownership.py")
BLOCKCHAIN_ROUTE = os.path.join(BASE_DIR, "api", "routes", "blockchain_routes.py")
BLOCKCHAIN_SERVICE = os.path.join(BASE_DIR, "services", "blockchain.py")

# Helper to read and write files
def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# Update Registration Service
reg_content = read_file(REG_SERVICE)
reg_content = reg_content.replace("from sqlalchemy.orm import Session", "from motor.motor_asyncio import AsyncIOMotorDatabase\nfrom bson import ObjectId")
reg_content = reg_content.replace("from app.models.document_model import RegisteredDocument, DocumentPage", "")
reg_content = reg_content.replace("from app.models.blockchain_model import BlockchainBlock", "")
reg_content = reg_content.replace("def _compute_similarity_breakdown(", "async def _compute_similarity_breakdown(")
reg_content = reg_content.replace("db: Session", "db: AsyncIOMotorDatabase")
reg_content = reg_content.replace("all_stored: List[DocumentPage] = db.query(DocumentPage).all()", "all_stored = await db.document_pages.find().to_list(length=None)")
reg_content = reg_content.replace("sp.page_hash", "sp['page_hash']")
reg_content = reg_content.replace("sp.embedding", "sp['embedding']")
reg_content = reg_content.replace("sp.document_id", "sp['document_id']")
reg_content = reg_content.replace("sp.page_number", "sp['page_number']")

reg_content = reg_content.replace("def get_doc(doc_id: int) -> RegisteredDocument:", "async def get_doc(doc_id: str):")
reg_content = reg_content.replace("doc_cache: Dict[int, RegisteredDocument] = {}", "doc_cache = {}")
reg_content = reg_content.replace("""            doc_cache[doc_id] = (
                db.query(RegisteredDocument)
                .filter(RegisteredDocument.id == doc_id)
                .first()
            )""", """            doc_cache[doc_id] = await db.documents.find_one({"_id": ObjectId(doc_id)})""")
reg_content = reg_content.replace("doc.owner_id", "doc['owner_id']")
reg_content = reg_content.replace("doc.owner_name", "doc['owner_name']")
reg_content = reg_content.replace("doc.filename", "doc['filename']")
reg_content = reg_content.replace("doc = get_doc", "doc = await get_doc")

reg_content = reg_content.replace("def register_document(", "async def register_document(")
reg_content = reg_content.replace("""    existing = (
        db.query(RegisteredDocument)
        .filter(RegisteredDocument.file_hash == file_hash_value)
        .first()
    )""", """    existing = await db.documents.find_one({"file_hash": file_hash_value})""")
reg_content = reg_content.replace("existing.owner_name", "existing['owner_name']")
reg_content = reg_content.replace("existing.owner_id", "existing['owner_id']")
reg_content = reg_content.replace("existing.registered_at.isoformat()", "existing['registered_at'].isoformat()")

reg_content = reg_content.replace("""    similarity_report = _compute_similarity_breakdown(pages, db)""", """    similarity_report = await _compute_similarity_breakdown(pages, db)""")

# DB Insert
reg_content = reg_content.replace("""    doc = RegisteredDocument(
        file_hash=file_hash_value,
        filename=filename,
        owner_id=owner_id,
        owner_name=owner_name,
        total_pages=total_pages,
        registered_at=datetime.now(timezone.utc),
    )
    db.add(doc)
    db.flush()  # Get doc.id before adding pages""", """    doc = {
        "file_hash": file_hash_value,
        "filename": filename,
        "owner_id": owner_id,
        "owner_name": owner_name,
        "total_pages": total_pages,
        "registered_at": datetime.now(timezone.utc)
    }
    res = await db.documents.insert_one(doc)
    doc_id = str(res.inserted_id)""")

reg_content = reg_content.replace("""        page_record = DocumentPage(
            document_id=doc.id,
            page_number=i + 1,
            page_hash=page_hash_value,
            embedding=EmbeddingService.serialize_embedding(embedding),
            page_text=page_text,
        )
        db.add(page_record)""", """        page_record = {
            "document_id": doc_id,
            "page_number": i + 1,
            "page_hash": page_hash_value,
            "embedding": EmbeddingService.serialize_embedding(embedding),
            "page_text": page_text
        }
        await db.document_pages.insert_one(page_record)""")
reg_content = reg_content.replace("    db.commit()", "")
reg_content = reg_content.replace("doc.registered_at.isoformat()", "doc['registered_at'].isoformat()")

reg_content = reg_content.replace("""    db_block = BlockchainBlock(
        block_index=block.index,
        block_hash=block.block_hash,
        previous_hash=block.previous_hash,
        file_hash=block.file_hash,
        owner_name=block.owner_name,
        timestamp=datetime.fromisoformat(block.timestamp),
    )
    db.add(db_block)
    db.commit()""", """    db_block = {
        "block_index": block.index,
        "block_hash": block.block_hash,
        "previous_hash": block.previous_hash,
        "file_hash": block.file_hash,
        "owner_name": block.owner_name,
        "timestamp": datetime.fromisoformat(block.timestamp),
    }
    await db.blockchain_blocks.insert_one(db_block)""")

write_file(REG_SERVICE, reg_content)

print("Updated registration_service.py")
