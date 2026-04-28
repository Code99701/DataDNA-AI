import os

BASE_DIR = r"d:\google solutions\Google-Solutions-2026-Project\backend_final\app"
MAIN_PY = os.path.join(BASE_DIR, "main.py")

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

content = """import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.api.routes.ownership import router as ownership_router
from app.api.routes.blockchain_routes import router as blockchain_router
from app.api.routes.auth import router as auth_router
from app.api.routes.admin import router as admin_router
from app.database.database import connect_db, close_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()

app = FastAPI(
    title="DataDNA AI",
    description="File Ownership Tracking & Verification Platform with Blockchain",
    version="3.0.0",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Include routers
app.include_router(ownership_router)
app.include_router(blockchain_router)
app.include_router(auth_router)
app.include_router(admin_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    \"\"\"Health check endpoint.\"\"\"
    return {
        "service": "DataDNA AI",
        "status": "running",
        "version": "3.0.0",
    }
"""

write_file(MAIN_PY, content)
print("Updated main.py")
