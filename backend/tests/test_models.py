"""
Tests for Pydantic models.

Tests the InternalTask model validation and behavior.
"""

import pytest
from pydantic import ValidationError
from src.core.domain.models import InternalTask, TaskStatus
from datetime import datetime


class TestInternalTaskModel:
    """Tests for InternalTask Pydantic model."""
    
    def test_internal_task_model_validation(self):
        """Test valid InternalTask creation."""
        # Arrange & Act
        task = InternalTask(
            booking_id=1,
            title="Valid task title"
        )
        
        # Assert
        assert task.booking_id == 1
        assert task.title == "Valid task title"
        assert task.status == TaskStatus.OPEN
        assert task.id is None
        assert isinstance(task.created_at, datetime)
    
    def test_internal_task_model_with_id(self):
        """Test InternalTask creation with ID."""
        # Arrange & Act
        task = InternalTask(
            id=1,
            booking_id=1,
            title="Task with ID",
            status=TaskStatus.IN_PROGRESS
        )
        
        # Assert
        assert task.id == 1
        assert task.booking_id == 1
        assert task.title == "Task with ID"
        assert task.status == TaskStatus.IN_PROGRESS
    
    def test_internal_task_model_status_validation(self):
        """Test TaskStatus validation."""
        # Test valid statuses
        for status in [TaskStatus.OPEN, TaskStatus.IN_PROGRESS, TaskStatus.CLOSED]:
            task = InternalTask(
                booking_id=1,
                title="Test task",
                status=status
            )
            assert task.status == status
        
        # Test invalid status (should work with string due to use_enum_values=True)
        task = InternalTask(
            booking_id=1,
            title="Test task",
            status="OPEN"
        )
        assert task.status == TaskStatus.OPEN
    
    def test_internal_task_model_title_validation(self):
        """Test title validation."""
        # Valid title
        task = InternalTask(
            booking_id=1,
            title="Valid Title"
        )
        assert task.title == "Valid Title"
        
        # Title with whitespace (should be stripped)
        task = InternalTask(
            booking_id=1,
            title="  Whitespace Title  "
        )
        assert task.title == "Whitespace Title"
        
        # Empty title (should raise ValidationError)
        with pytest.raises(ValidationError) as exc_info:
            InternalTask(
                booking_id=1,
                title=""
            )
        assert "Title must not be empty" in str(exc_info.value)
        
        # Whitespace-only title (should raise ValidationError)
        with pytest.raises(ValidationError) as exc_info:
            InternalTask(
                booking_id=1,
                title="   "
            )
        assert "Title must not be empty" in str(exc_info.value)
    
    def test_internal_task_model_booking_id_validation(self):
        """Test booking_id validation."""
        # Valid booking_id
        task = InternalTask(
            booking_id=1,
            title="Valid task"
        )
        assert task.booking_id == 1
        
        # Zero booking_id (should raise ValidationError)
        with pytest.raises(ValidationError):
            InternalTask(
                booking_id=0,
                title="Invalid task"
            )
        
        # Negative booking_id (should raise ValidationError)
        with pytest.raises(ValidationError):
            InternalTask(
                booking_id=-1,
                title="Invalid task"
            )
    
    def test_internal_task_model_defaults(self):
        """Test default values."""
        # Arrange & Act
        task = InternalTask(
            booking_id=123,
            title="Test task for defaults"
        )
        
        # Assert
        assert task.id is None
        assert task.booking_id == 123
        assert task.title == "Test task for defaults"
        assert task.status == TaskStatus.OPEN  # Default status
        assert isinstance(task.created_at, datetime)
    
    def test_internal_task_model_json_serialization(self):
        """Test JSON serialization."""
        # Arrange
        task = InternalTask(
            id=1,
            booking_id=1,
            title="JSON test",
            status=TaskStatus.CLOSED
        )
        
        # Act
        json_data = task.dict()
        
        # Assert
        assert json_data["id"] == 1
        assert json_data["booking_id"] == 1
        assert json_data["title"] == "JSON test"
        assert json_data["status"] == "CLOSED"  # Enum value
        assert "created_at" in json_data