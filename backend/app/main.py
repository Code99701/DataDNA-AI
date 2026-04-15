from fastapi import FastAPI

from app.api.routes import upload, detect
from app.api.routes import biometric

app = FastAPI(title="DataDNA AI")

app.include_router(biometric.router)

# Include routers
app.include_router(upload.router)
app.include_router(detect.router)