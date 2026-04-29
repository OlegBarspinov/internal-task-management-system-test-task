"""
InternalTask domain model.

Defines the InternalTask entity with business logic and validation rules.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict, field_serializer


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
    title: str = Field(..., description="Task title", max_length=255)
    status: TaskStatus = Field(default=TaskStatus.OPEN, description="Task status")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    
    @field_validator('title', mode='after')
    def title_must_not_be_empty(cls, v):
        """Validate that title is not empty or just whitespace."""
        if not v or not v.strip():
            raise ValueError('Title must not be empty')
        return v.strip()
    
    model_config = ConfigDict(
        use_enum_values=True,
    )

    @field_serializer('created_at')
    def serialize_created_at(self, v: datetime) -> str:
        """Serialize datetime to ISO format string."""
        return v.isoformat() if v else None