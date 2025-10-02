from fastapi import FastAPI
from .service import router as service_router

app = FastAPI(
    title="AI Service for Hakaton 2025"
)

app.include_router(service_router, prefix="/api")
