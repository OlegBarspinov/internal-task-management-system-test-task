"""
Use case for creating a new task.

Implements business logic for task creation with duplicate prevention.
"""

from src.core.interfaces.repositories import ITaskRepository
from src.core.domain.models import InternalTask, TaskStatus


class CreateTaskUseCase:
    """
    Use case for creating a new task.
    
    Responsibilities:
    - Validate task data
    - Check for duplicates
    - Create task via repository
    - Apply business rules
    """
    
    def __init__(self, task_repository: ITaskRepository):
        """
        Initialize use case with task repository.
        
        Args:
            task_repository: Repository for task data access
        """
        self.task_repository = task_repository
    
    def execute(self, booking_id: int, title: str) -> InternalTask:
        """
        Create a new task.
        
        Args:
            booking_id: The booking identifier
            title: The task title/description
            
        Returns:
            The created task
            
        Raises:
            ValueError: If task is duplicate or validation fails
            Exception: For repository errors
        """
        # Create task domain object for validation and processing
        task = InternalTask(
            booking_id=booking_id,
            title=title,
            status=TaskStatus.OPEN
        )
        
        # Check for duplicate task (same booking_id + title)
        if self.task_repository.exists(booking_id, title.strip()):
            raise ValueError(f"Task with title '{title}' already exists for booking {booking_id}")
        
        # Create task via repository
        created_task = self.task_repository.create(task)
        
        return created_task