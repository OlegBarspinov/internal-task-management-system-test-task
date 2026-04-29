"""
Basic API endpoints.

Defines basic REST API endpoints for health checks and root information.
"""

from fastapi import APIRouter


router = APIRouter(tags=["basic"])


@router.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "message": "Internal Task Management API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}