"""
Tests for repository layer.

Tests the SQLAlchemy repository implementation for task operations.
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.repositories.tasks import SQLAlchemyTaskRepository
from src.infrastructure.database.models import Base, InternalTaskTable
from src.core.domain.models import InternalTask, TaskStatus


@pytest.mark.asyncio
class TestSQLAlchemyTaskRepository:
    """Tests for SQLAlchemyTaskRepository implementation."""
    
    async def test_create_and_retrieve_task(self, test_db_session: AsyncSession):
        """Test creating and retrieving a task."""
        # Arrange
        repository = SQLAlchemyTaskRepository(test_db_session)
        task_data = InternalTask(
            booking_id=1,
            title="Test task",
            status=TaskStatus.OPEN
        )
        
        # Act
        created_task = await repository.create(task_data)
        retrieved_task = await repository.get_by_id(created_task.id)
        
        # Assert
        assert created_task.id is not None
        assert created_task.booking_id == 1
        assert created_task.title == "Test task"
        assert created_task.status == TaskStatus.OPEN
        
        assert retrieved_task is not None
        assert retrieved_task.id == created_task.id
        assert retrieved_task.booking_id == created_task.booking_id
        assert retrieved_task.title == created_task.title
        assert retrieved_task.status == created_task.status
    
    async def test_exists_duplicate(self, test_db_session: AsyncSession):
        """Test duplicate detection."""
        # Arrange
        repository = SQLAlchemyTaskRepository(test_db_session)
        task_data = InternalTask(
            booking_id=1,
            title="Duplicate test",
            status=TaskStatus.OPEN
        )
        
        # Act - Create first task
        await repository.create(task_data)
        
        # Check for duplicate
        exists = await repository.exists(1, "Duplicate test")
        
        # Assert
        assert exists is True
        
        # Check non-duplicate
        exists_not = await repository.exists(1, "Different title")
        assert exists_not is False
        
        # Check different booking
        exists_other_booking = await repository.exists(2, "Duplicate test")
        assert exists_other_booking is False
    
    async def test_update_status_repository(self, test_db_session: AsyncSession):
        """Test updating task status at repository level."""
        # Arrange
        repository = SQLAlchemyTaskRepository(test_db_session)
        task_data = InternalTask(
            booking_id=1,
            title="Task to update",
            status=TaskStatus.OPEN
        )
        
        # Act - Create task
        created_task = await repository.create(task_data)
        
        # Update status
        updated_task = await repository.update_status(created_task.id, "IN_PROGRESS")
        
        # Assert
        assert updated_task.id == created_task.id
        assert updated_task.status == TaskStatus.IN_PROGRESS
        assert updated_task.title == created_task.title
        assert updated_task.booking_id == created_task.booking_id
    
    async def test_get_by_booking_id_empty(self, test_db_session: AsyncSession):
        """Test getting tasks for booking with no tasks."""
        # Arrange
        repository = SQLAlchemyTaskRepository(test_db_session)
        
        # Act
        tasks = await repository.get_by_booking_id(999)
        
        # Assert
        assert tasks == []
    
    async def test_get_by_id_not_found(self, test_db_session: AsyncSession):
        """Test getting non-existent task by ID."""
        # Arrange
        repository = SQLAlchemyTaskRepository(test_db_session)
        
        # Act
        task = await repository.get_by_id(999)
        
        # Assert
        assert task is None