"""
Abstract repository interface for task operations.

Defines the contract for data access operations without implementation details.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from src.core.domain.models import InternalTask


class ITaskRepository(ABC):
    """
    Abstract interface for task repository operations.
    
    This interface defines the contract for data access operations.
    Implementations should be provided in the infrastructure layer.
    """
    
    @abstractmethod
    def create(self, task: InternalTask) -> InternalTask:
        """
        Create a new task.
        
        Args:
            task: The task to create
            
        Returns:
            The created task with generated ID
            
        Raises:
            ValueError: If task validation fails
            Exception: For database errors
        """
        pass
    
    @abstractmethod
    def get_by_booking_id(self, booking_id: int) -> List[InternalTask]:
        """
        Get all tasks for a specific booking.
        
        Args:
            booking_id: The booking identifier
            
        Returns:
            List of tasks for the booking (empty list if none found)
        """
        pass
    
    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[InternalTask]:
        """
        Get a task by its ID.
        
        Args:
            task_id: The task identifier
            
        Returns:
            The task if found, None otherwise
        """
        pass
    
    @abstractmethod
    def update_status(self, task_id: int, status: str) -> InternalTask:
        """
        Update the status of a task.
        
        Args:
            task_id: The task identifier
            status: The new status value
            
        Returns:
            The updated task
            
        Raises:
            ValueError: If task not found or invalid status
            Exception: For database errors
        """
        pass
    
    @abstractmethod
    def exists(self, booking_id: int, title: str) -> bool:
        """
        Check if a task with the same booking_id and title already exists.
        
        Args:
            booking_id: The booking identifier
            title: The task title
            
        Returns:
            True if duplicate exists, False otherwise
        """
        pass