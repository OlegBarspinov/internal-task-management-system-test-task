"""
FastAPI application entry point.

Sets up the FastAPI app, includes routers, and configures dependencies.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.app.api import tasks
from src.infrastructure.logging import logger


# Create FastAPI application
app = FastAPI(
    title="Internal Task Management API",
    description="API for managing internal tasks related to bookings",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(tasks.router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    logger.info("Starting Internal Task Management API")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event."""
    logger.info("Shutting down Internal Task Management API")


@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "message": "Internal Task Management API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}