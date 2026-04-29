"""
API request/response schemas.

Pydantic models for request validation and response serialization.
"""

from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Generic, TypeVar, List, Optional

from ...core.domain.models import TaskStatus


T = TypeVar('T')


class CreateTaskRequest(BaseModel):
    """Request model for creating a task."""
    title: str = Field(..., min_length=1, max_length=255, description="Task title")


class UpdateTaskStatusRequest(BaseModel):
    """Request model for updating task status."""
    status: str = Field(..., description="New task status (OPEN, IN_PROGRESS, CLOSED)")


# Response schemas
class TaskResponse(BaseModel):
    """Standardized task response."""
    id: int
    booking_id: int
    title: str
    status: TaskStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ApiResponse(BaseModel, Generic[T]):
    """Generic API response wrapper."""
    success: bool = True
    data: Optional[T] = None
    message: Optional[str] = None
    error: Optional[str] = None


class ErrorResponse(BaseModel):
    """Standardized error response."""
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
