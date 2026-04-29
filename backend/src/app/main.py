"""
FastAPI application entry point.

Sets up the FastAPI app, includes routers, and configures dependencies.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from .api import tasks, basic
from .exceptions import (
    app_exception_handler,
    integrity_error_handler,
    generic_exception_handler,
    AppException
)
from ..infrastructure.logging import logger
from ..infrastructure.database.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting Internal Task Management API (from lifespan)") # Added specific log
    try:
        logger.info("Attempting to initialize database...")
        await init_db()  # Call init_db here to create tables
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Error during database initialization: {e}", exc_info=True)
        # Depending on desired behavior, you might want to re-raise or exit here
        # For now, we'll just log and continue, but the app might not function correctly.
    yield
    # Shutdown
    logger.info("Shutting down Internal Task Management API")


# Create FastAPI application
app = FastAPI(
    title="Internal Task Management API",
    description="API for managing internal tasks related to bookings",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Include routers
app.include_router(basic.router)
app.include_router(tasks.router, prefix="/api/v1")
