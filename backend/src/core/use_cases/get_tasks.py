"""
Use case for retrieving tasks by booking ID.

Implements business logic for getting tasks associated with a booking.
"""

from typing import List
from src.core.interfaces.repositories import ITaskRepository
from src.core.domain.models import InternalTask


class GetTasksUseCase:
    """
    Use case for retrieving tasks by booking ID.
    
    Responsibilities:
    - Get tasks for a specific booking
    - Return empty list if no tasks found
    """
    
    def __init__(self, task_repository: ITaskRepository):
        """
        Initialize use case with task repository.
        
        Args:
            task_repository: Repository for task data access
        """
        self.task_repository = task_repository
    
    def execute(self, booking_id: int) -> List[InternalTask]:
        """
        Get all tasks for a specific booking.
        
        Args:
            booking_id: The booking identifier
            
        Returns:
            List of tasks for the booking (empty list if none found)
        """
        return self.task_repository.get_by_booking_id(booking_id)