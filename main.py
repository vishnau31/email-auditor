from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger

from app.api import upload_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Email Audit Service starting up...")
    yield
    logger.info("Email Audit Service shutting down...")


app = FastAPI(
    title="Email Audit Service",
    description="A service for auditing email communication quality using dynamic rules",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Email Audit Service",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "email-audit-service",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 