"""
Exception handlers for the application.

Centralized error handling for consistent error responses.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from typing import Union

from ..infrastructure.logging import logger


class AppException(Exception):
    """Base application exception."""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class DuplicateTaskError(AppException):
    """Raised when attempting to create a duplicate task."""
    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_409_CONFLICT)


class TaskNotFoundError(AppException):
    """Raised when a task is not found."""
    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)


class InvalidStatusError(AppException):
    """Raised when an invalid status is provided."""
    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_400_BAD_REQUEST)


async def app_exception_handler(request: Request, exc: AppException):
    """Handle application-specific exceptions."""
    # Log error type and status code, but avoid logging sensitive data (e.g., task titles)
    logger.error(
        f"Application error: {exc.__class__.__name__} (status={exc.status_code}): {exc.message}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Handle database integrity errors (e.g., unique constraint violations)."""
    error_message = "Database integrity error"
    
    # Check for unique constraint violation
    if "uix_booking_title" in str(exc):
        error_message = "Task with this title already exists for this booking"
        logger.warning(f"Duplicate task attempt detected (unique constraint violation)")
    else:
        logger.error(f"Database integrity error: {type(exc).__name__}")
    
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": error_message}
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    logger.error(
        f"Unexpected error: {type(exc).__name__}: {str(exc)}",
        exc_info=True
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )
