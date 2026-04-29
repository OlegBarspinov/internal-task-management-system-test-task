"""
Tests for business logic (use cases).

Tests the use case implementations with mocked dependencies.
"""

from unittest.mock import Mock, AsyncMock
import pytest
from pydantic import ValidationError

from src.core.use_cases.create_task import CreateTaskUseCase
from src.core.use_cases.get_tasks import GetTasksUseCase
from src.core.use_cases.update_task import UpdateTaskUseCase
from src.core.interfaces.repositories import ITaskRepository
from src.core.domain.models import InternalTask, TaskStatus


class TestCreateTaskUseCase:
    """Tests for CreateTaskUseCase."""
    
    def test_create_task_use_case_success(self):
        """Test successful task creation via use case."""
        import asyncio
        
        # Arrange
        mock_repo = Mock(spec=ITaskRepository)
        mock_repo.exists = AsyncMock(return_value=False)  # No duplicate
        mock_repo.create = AsyncMock(return_value=InternalTask(
            id=1,
            booking_id=1,
            title="Test task",
            status=TaskStatus.OPEN
        ))
        
        use_case = CreateTaskUseCase(mock_repo)
        
        # Act
        result = asyncio.run(use_case.execute(booking_id=1, title="Test task"))
        
        # Assert
        assert result.id == 1
        assert result.booking_id == 1
        assert result.title == "Test task"
        assert result.status == TaskStatus.OPEN
        
        mock_repo.exists.assert_called_once_with(1, "Test task")
        mock_repo.create.assert_called_once()
    
    def test_create_task_use_case_duplicate(self):
        """Test duplicate task prevention via use case."""
        import asyncio
        
        # Arrange
        mock_repo = Mock(spec=ITaskRepository)
        mock_repo.exists = AsyncMock(return_value=True)  # Duplicate exists
        
        use_case = CreateTaskUseCase(mock_repo)
        
        # Act & Assert
        with pytest.raises(ValueError, match="already exists"):
            asyncio.run(use_case.execute(booking_id=1, title="Duplicate task"))
        
        mock_repo.exists.assert_called_once_with(1, "Duplicate task")
        mock_repo.create.assert_not_called()  # Should not call create
    
    def test_create_task_use_case_empty_title(self):
        """Test task creation with empty title via use case."""
        import asyncio
        
        # Arrange
        mock_repo = Mock(spec=ITaskRepository)
        use_case = CreateTaskUseCase(mock_repo)
        
        # Act & Assert
        with pytest.raises(ValueError, match="Title must not be empty"):
            asyncio.run(use_case.execute(booking_id=1, title=""))


class TestGetTasksUseCase:
    """Tests for GetTasksUseCase."""
    
    def test_get_tasks_use_case_success(self):
        """Test successful task retrieval via use case."""
        import asyncio
        
        # Arrange
        mock_repo = Mock(spec=ITaskRepository)
        mock_tasks = [
            InternalTask(id=1, booking_id=1, title="Task 1", status=TaskStatus.OPEN),
            InternalTask(id=2, booking_id=1, title="Task 2", status=TaskStatus.CLOSED)
        ]
        mock_repo.get_by_booking_id = AsyncMock(return_value=mock_tasks)
        
        use_case = GetTasksUseCase(mock_repo)
        
        # Act
        result = asyncio.run(use_case.execute(booking_id=1))
        
        # Assert
        assert len(result) == 2
        assert result[0].id == 1
        assert result[0].title == "Task 1"
        assert result[1].id == 2
        assert result[1].title == "Task 2"
        
        mock_repo.get_by_booking_id.assert_called_once_with(1)
    
    def test_get_tasks_use_case_empty(self):
        """Test getting tasks when none exist."""
        import asyncio
        
        # Arrange
        mock_repo = Mock(spec=ITaskRepository)
        mock_repo.get_by_booking_id = AsyncMock(return_value=[])
        
        use_case = GetTasksUseCase(mock_repo)
        
        # Act
        result = asyncio.run(use_case.execute(booking_id=999))
        
        # Assert
        assert result == []
        mock_repo.get_by_booking_id.assert_called_once_with(999)


class TestUpdateTaskUseCase:
    """Tests for UpdateTaskUseCase."""
    
    def test_update_task_use_case_success(self):
        """Test successful task status update via use case."""
        import asyncio
        
        # Arrange
        mock_repo = Mock(spec=ITaskRepository)
        mock_repo.get_by_id = AsyncMock(return_value=InternalTask(
            id=1,
            booking_id=1,
            title="Test task",
            status=TaskStatus.OPEN
        ))
        mock_repo.update_status = AsyncMock(return_value=InternalTask(
            id=1,
            booking_id=1,
            title="Test task",
            status=TaskStatus.IN_PROGRESS
        ))
        
        use_case = UpdateTaskUseCase(mock_repo)
        
        # Act
        result = asyncio.run(use_case.execute(task_id=1, status="IN_PROGRESS"))
        
        # Assert
        assert result.id == 1
        assert result.status == TaskStatus.IN_PROGRESS
        assert result.title == "Test task"
        
        mock_repo.get_by_id.assert_called_once_with(1)
        mock_repo.update_status.assert_called_once_with(1, "IN_PROGRESS")
    
    def test_update_task_use_case_not_found(self):
        """Test updating non-existent task via use case."""
        import asyncio
        
        # Arrange
        mock_repo = Mock(spec=ITaskRepository)
        mock_repo.get_by_id = AsyncMock(return_value=None)  # Not found
        
        use_case = UpdateTaskUseCase(mock_repo)
        
        # Act & Assert
        with pytest.raises(ValueError, match="not found"):
            asyncio.run(use_case.execute(task_id=999, status="IN_PROGRESS"))
        
        mock_repo.get_by_id.assert_called_once_with(999)
        mock_repo.update_status.assert_not_called()
    
    def test_update_task_use_case_invalid_status(self):
        """Test updating task with invalid status via use case."""
        import asyncio
        
        # Arrange
        mock_repo = Mock(spec=ITaskRepository)
        
        use_case = UpdateTaskUseCase(mock_repo)
        
        # Act & Assert
        with pytest.raises(ValueError, match="Invalid status"):
            asyncio.run(use_case.execute(task_id=1, status="INVALID_STATUS"))
        
        mock_repo.get_by_id.assert_not_called()
        mock_repo.update_status.assert_not_called()
