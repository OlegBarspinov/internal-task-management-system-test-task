"""
Use case for updating task status.

Implements business logic for updating task status with validation.
"""

from ..interfaces.repositories import ITaskRepository
from ..domain.models import InternalTask, TaskStatus


class UpdateTaskUseCase:
    """
    Use case for updating task status.
    
    Responsibilities:
    - Validate task exists
    - Validate status transition
    - Update task via repository
    """
    
    def __init__(self, task_repository: ITaskRepository):
        """
        Initialize use case with task repository.
        
        Args:
            task_repository: Repository for task data access
        """
        self.task_repository = task_repository
    
    async def execute(self, task_id: int, status: str) -> InternalTask:
        """
        Update the status of a task.
        
        Args:
            task_id: The task identifier
            status: The new status value
            
        Returns:
            The updated task
            
        Raises:
            ValueError: If task not found or invalid status
            Exception: For repository errors
        """
        # Validate status is a valid TaskStatus
        try:
            task_status = TaskStatus(status)
        except ValueError:
            valid_statuses = [s.value for s in TaskStatus]
            raise ValueError(f"Invalid status '{status}'. Valid statuses: {valid_statuses}")
        
        # Get existing task
        existing_task = await self.task_repository.get_by_id(task_id)
        if not existing_task:
            raise ValueError(f"Task with ID {task_id} not found")
        
        # Update task status via repository
        updated_task = await self.task_repository.update_status(task_id, task_status.value)
        
        return updated_task