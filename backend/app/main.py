from fastapi import FastAPI

from backend.app.api.routes import upload, detect

app = FastAPI(title="DataDNA AI")

# Include routers
app.include_router(upload.router)
app.include_router(detect.router)