"""
SQLAlchemy implementation of the task repository.

Concrete implementation of ITaskRepository using SQLAlchemy ORM.
"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ....core.interfaces.repositories import ITaskRepository
from ....core.domain.models import InternalTask
from ..models import InternalTaskTable


class SQLAlchemyTaskRepository(ITaskRepository):
    """
    SQLAlchemy implementation of the task repository.
    
    Handles conversion between domain entities and database models.
    """
    
    def __init__(self, session: AsyncSession):
        """
        Initialize repository with database session.
        
        Args:
            session: Async SQLAlchemy session
        """
        self.session = session
    
    async def create(self, task: InternalTask) -> InternalTask:
        """
        Create a new task in the database.
        
        Args:
            task: The task domain entity to create
            
        Returns:
            The created task with generated ID
        """
        # Convert domain model to database model
        db_task = InternalTaskTable(
            booking_id=task.booking_id,
            title=task.title,
            status=task.status,
            created_at=task.created_at
        )
        
        # Add to session and commit
        self.session.add(db_task)
        await self.session.commit()
        await self.session.refresh(db_task)
        
        return InternalTask(
            id=db_task.id,
            booking_id=db_task.booking_id,
            title=db_task.title,
            status=db_task.status,
            created_at=db_task.created_at
        )
    
    async def get_by_booking_id(self, booking_id: int) -> List[InternalTask]:
        """
        Get all tasks for a specific booking.
        
        Args:
            booking_id: The booking identifier
            
        Returns:
            List of tasks for the booking
        """
        result = await self.session.execute(
            select(InternalTaskTable).where(InternalTaskTable.booking_id == booking_id)
        )
        db_tasks = result.scalars().all()
        
        return [
            InternalTask(
                id=db_task.id,
                booking_id=db_task.booking_id,
                title=db_task.title,
                status=db_task.status,
                created_at=db_task.created_at
            )
            for db_task in db_tasks
        ]
    
    async def get_by_id(self, task_id: int) -> Optional[InternalTask]:
        """
        Get a task by its ID.
        
        Args:
            task_id: The task identifier
            
        Returns:
            The task if found, None otherwise
        """
        result = await self.session.execute(
            select(InternalTaskTable).where(InternalTaskTable.id == task_id)
        )
        db_task = result.scalar_one_or_none()
        
        if not db_task:
            return None
            
        return InternalTask(
            id=db_task.id,
            booking_id=db_task.booking_id,
            title=db_task.title,
            status=db_task.status,
            created_at=db_task.created_at
        )
    
    async def update_status(self, task_id: int, status: str) -> InternalTask:
        """
        Update the status of a task.
        
        Args:
            task_id: The task identifier
            status: The new status value
            
        Returns:
            The updated task
        """
        result = await self.session.execute(
            select(InternalTaskTable).where(InternalTaskTable.id == task_id)
        )
        db_task = result.scalar_one_or_none()
        
        if not db_task:
            raise ValueError(f"Task with ID {task_id} not found")
        
        db_task.status = status
        
        await self.session.commit()
        await self.session.refresh(db_task)
        
        return InternalTask(
            id=db_task.id,
            booking_id=db_task.booking_id,
            title=db_task.title,
            status=db_task.status,
            created_at=db_task.created_at
        )
    
    async def exists(self, booking_id: int, title: str) -> bool:
        """
        Check if a task with the same booking_id and title already exists.
        
        Args:
            booking_id: The booking identifier
            title: The task title
            
        Returns:
            True if duplicate exists, False otherwise
        """
        result = await self.session.execute(
            select(InternalTaskTable).where(
                InternalTaskTable.booking_id == booking_id,
                InternalTaskTable.title == title.strip()
            )
        )
        db_task = result.scalar_one_or_none()
        
        return db_task is not None