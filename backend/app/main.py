from fastapi import FastAPI

from app.api.routes import upload, detect
from app.api.routes import biometric
from app.api.routes.register import router as register_router
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="DataDNA AI")

app.include_router(biometric.router)
app.include_router(register_router)
# Include routers
app.include_router(upload.router)
app.include_router(detect.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)