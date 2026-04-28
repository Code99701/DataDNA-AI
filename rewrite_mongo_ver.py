import os

BASE_DIR = r"d:\google solutions\Google-Solutions-2026-Project\backend_final\app"
VER_SERVICE = os.path.join(BASE_DIR, "services", "verification_service.py")

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

content = read_file(VER_SERVICE)

# Imports
content = content.replace("from sqlalchemy.orm import Session", "from motor.motor_asyncio import AsyncIOMotorDatabase\nfrom bson import ObjectId")
content = content.replace("from app.models.document_model import RegisteredDocument, DocumentPage", "")

# verify_document
content = content.replace("def verify_document(", "async def verify_document(")
content = content.replace("db: Session", "db: AsyncIOMotorDatabase")
content = content.replace("""    exact_match = (
        db.query(RegisteredDocument)
        .filter(RegisteredDocument.file_hash == file_hash_value)
        .first()
    )""", """    exact_match = await db.documents.find_one({"file_hash": file_hash_value})""")
content = content.replace("exact_match.owner_name", "exact_match['owner_name']")
content = content.replace("exact_match.owner_id", "exact_match['owner_id']")

# Load stored pages
content = content.replace("""    all_stored_pages: List[DocumentPage] = (
        db.query(DocumentPage).all()
    )""", """    all_stored_pages = await db.document_pages.find().to_list(length=None)""")

content = content.replace("sp.page_hash", "sp['page_hash']")
content = content.replace("sp.embedding", "sp['embedding']")
content = content.replace("sp.document_id", "sp['document_id']")
content = content.replace("sp.page_number", "sp['page_number']")

content = content.replace("def get_doc(doc_id: int) -> RegisteredDocument:", "async def get_doc(doc_id: str):")
content = content.replace("doc_cache: Dict[int, RegisteredDocument] = {}", "doc_cache = {}")
content = content.replace("""            doc_cache[doc_id] = (
                db.query(RegisteredDocument)
                .filter(RegisteredDocument.id == doc_id)
                .first()
            )""", """            doc_cache[doc_id] = await db.documents.find_one({"_id": ObjectId(doc_id)})""")

content = content.replace("doc.owner_id", "doc['owner_id']")
content = content.replace("doc.owner_name", "doc['owner_name']")
content = content.replace("doc.filename", "doc['filename']")
content = content.replace("doc = get_doc", "doc = await get_doc")

# Chunks analysis
content = content.replace("def _analyze_chunks(", "async def _analyze_chunks(")
content = content.replace("stored_page: DocumentPage", "stored_page: dict")
content = content.replace("doc: RegisteredDocument", "doc: dict")
content = content.replace("db: Session", "db: AsyncIOMotorDatabase")
content = content.replace("stored_page.page_text", "stored_page.get('page_text')")
content = content.replace("_analyze_chunks(", "await _analyze_chunks(")

write_file(VER_SERVICE, content)
print("Updated verification_service.py")
