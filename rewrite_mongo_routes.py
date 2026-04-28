import os

BASE_DIR = r"d:\google solutions\Google-Solutions-2026-Project\backend_final\app"
OWNERSHIP_ROUTE = os.path.join(BASE_DIR, "api", "routes", "ownership.py")
BLOCKCHAIN_ROUTE = os.path.join(BASE_DIR, "api", "routes", "blockchain_routes.py")

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# OWNERSHIP ROUTE
content = read_file(OWNERSHIP_ROUTE)
content = content.replace("from sqlalchemy.orm import Session", "from motor.motor_asyncio import AsyncIOMotorDatabase\nfrom app.api.dependencies import get_current_user\nfrom app.models.auth_models import UserDocument")
content = content.replace("from app.database.db import get_db", "from app.database.database import get_db")
content = content.replace("from app.models.document_model import RegisteredDocument, DocumentPage", "")

content = content.replace("db: Session = Depends(get_db),", "db: AsyncIOMotorDatabase = Depends(get_db),\n    current_user: UserDocument = Depends(get_current_user),")

content = content.replace("result = register_document(", "result = await register_document(")
content = content.replace("result = verify_document(", "result = await verify_document(")

# Documents list
content = content.replace("""    query = db.query(RegisteredDocument)

    if owner_id:
        query = query.filter(RegisteredDocument.owner_id == owner_id)

    documents = query.order_by(RegisteredDocument.registered_at.desc()).all()""", """    match = {}
    if owner_id:
        match["owner_id"] = owner_id
    documents = await db.documents.find(match).sort("registered_at", -1).to_list(length=None)""")
content = content.replace("doc.id", "str(doc['_id'])")
content = content.replace("doc.file_hash", "doc['file_hash']")
content = content.replace("doc.filename", "doc['filename']")
content = content.replace("doc.owner_id", "doc['owner_id']")
content = content.replace("doc.owner_name", "doc['owner_name']")
content = content.replace("doc.total_pages", "doc['total_pages']")
content = content.replace("doc.registered_at.isoformat()", "doc['registered_at'].isoformat()")

# Document details
content = content.replace("""    doc = (
        db.query(RegisteredDocument)
        .filter(RegisteredDocument.file_hash == file_hash)
        .first()
    )""", """    doc = await db.documents.find_one({"file_hash": file_hash})""")
content = content.replace("""    pages = (
        db.query(DocumentPage)
        .filter(DocumentPage.document_id == doc.id)
        .order_by(DocumentPage.page_number)
        .all()
    )""", """    pages = await db.document_pages.find({"document_id": str(doc["_id"])}).sort("page_number", 1).to_list(length=None)""")

content = content.replace("p.page_number", "p['page_number']")
content = content.replace("p.page_hash", "p['page_hash']")
content = content.replace("p.embedding is not None", "p.get('embedding') is not None")
content = content.replace("p.page_text", "p.get('page_text')")

write_file(OWNERSHIP_ROUTE, content)
print("Updated ownership.py")

# BLOCKCHAIN ROUTE
content = read_file(BLOCKCHAIN_ROUTE)
content = content.replace("from app.api.dependencies import get_current_user\nfrom app.models.auth_models import UserDocument", "") # clear to avoid duplicates if rerun
content = content.replace("from fastapi import APIRouter, HTTPException", "from fastapi import APIRouter, HTTPException, Depends\nfrom app.api.dependencies import get_current_user\nfrom app.models.auth_models import UserDocument")

content = content.replace("def get_chain():", "async def get_chain(current_user: UserDocument = Depends(get_current_user)):")
content = content.replace("def verify_chain():", "async def verify_chain(current_user: UserDocument = Depends(get_current_user)):")
content = content.replace("def get_block(", "async def get_block(")
content = content.replace("def get_owner_blocks(", "async def get_owner_blocks(")
content = content.replace("file_hash: str,", "file_hash: str,\n    current_user: UserDocument = Depends(get_current_user),")
content = content.replace("owner_name: str,", "owner_name: str,\n    current_user: UserDocument = Depends(get_current_user),")

write_file(BLOCKCHAIN_ROUTE, content)
print("Updated blockchain_routes.py")
