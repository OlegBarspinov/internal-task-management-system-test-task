"""
InternalTask domain model.

Defines the InternalTask entity with business logic and validation rules.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, validator


class TaskStatus(str, Enum):
    """Task status enumeration."""
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    CLOSED = "CLOSED"


class InternalTask(BaseModel):
    """
    Internal task entity for tracking operational issues.
    
    Attributes:
        id: Unique identifier (auto-generated)
        booking_id: Reference to booking
        title: Task title/description
        status: Current task status
        created_at: Timestamp when task was created
    """
    
    id: Optional[int] = Field(None, description="Unique identifier")
    booking_id: int = Field(..., description="Booking identifier", gt=0)
    title: str = Field(..., description="Task title", min_length=1, max_length=255)
    status: TaskStatus = Field(default=TaskStatus.OPEN, description="Task status")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    
    @validator('title')
    def title_must_not_be_empty(cls, v):
        """Validate that title is not empty or just whitespace."""
        if not v or not v.strip():
            raise ValueError('Title must not be empty')
        return v.strip()
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }