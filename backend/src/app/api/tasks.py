"""
Task API endpoints.

Defines REST API endpoints for task management operations.
"""

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.core.use_cases.create_task import CreateTaskUseCase
from src.core.use_cases.get_tasks import GetTasksUseCase
from src.core.use_cases.update_task import UpdateTaskUseCase
from src.infrastructure.database.database import get_db_session
from src.infrastructure.database.repositories.tasks import SQLAlchemyTaskRepository
from src.core.domain.models import InternalTask, TaskStatus
from src.infrastructure.logging import logger


# Create router
router = APIRouter(prefix="/bookings/{booking_id}/tasks", tags=["tasks"])


def get_task_repository(db: AsyncSession = Depends(get_db_session)) -> SQLAlchemyTaskRepository:
    """
    Dependency that provides a task repository instance.
    
    Args:
        db: Database session dependency
        
    Returns:
        SQLAlchemyTaskRepository: Repository instance
    """
    return SQLAlchemyTaskRepository(db)


def get_create_task_use_case(
    repo: SQLAlchemyTaskRepository = Depends(get_task_repository)
) -> CreateTaskUseCase:
    """
    Dependency that provides a create task use case instance.
    
    Args:
        repo: Task repository dependency
        
    Returns:
        CreateTaskUseCase: Use case instance
    """
    return CreateTaskUseCase(repo)


def get_get_tasks_use_case(
    repo: SQLAlchemyTaskRepository = Depends(get_task_repository)
) -> GetTasksUseCase:
    """
    Dependency that provides a get tasks use case instance.
    
    Args:
        repo: Task repository dependency
        
    Returns:
        GetTasksUseCase: Use case instance
    """
    return GetTasksUseCase(repo)


def get_update_task_use_case(
    repo: SQLAlchemyTaskRepository = Depends(get_task_repository)
) -> UpdateTaskUseCase:
    """
    Dependency that provides an update task use case instance.
    
    Args:
        repo: Task repository dependency
        
    Returns:
        UpdateTaskUseCase: Use case instance
    """
    return UpdateTaskUseCase(repo)


@router.post("/", response_model=InternalTask, status_code=status.HTTP_201_CREATED)
async def create_task(
    booking_id: int = Path(..., gt=0, description="Booking ID"),
    title: str = ...,  # Will be extracted from request body
    use_case: CreateTaskUseCase = Depends(get_create_task_use_case)
):
    """
    Create a new task for a booking.
    
    Args:
        booking_id: The booking identifier (path parameter)
        title: The task title (request body)
        use_case: Create task use case dependency
        
    Returns:
        InternalTask: The created task
        
    Raises:
        HTTPException: 409 if duplicate task, 422 for validation errors
    """
    logger.info(f"Creating task for booking {booking_id} with title: {title}")
    
    try:
        task = use_case.execute(booking_id=booking_id, title=title)
        logger.info(f"Task created successfully with ID: {task.id}")
        return task
    except ValueError as e:
        logger.warning(f"Failed to create task: {str(e)}")
        if "already exists" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e)
            )
    except Exception as e:
        logger.error(f"Unexpected error creating task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/", response_model=List[InternalTask])
async def get_tasks(
    booking_id: int = Path(..., gt=0, description="Booking ID"),
    use_case: GetTasksUseCase = Depends(get_get_tasks_use_case)
):
    """
    Get all tasks for a booking.
    
    Args:
        booking_id: The booking identifier (path parameter)
        use_case: Get tasks use case dependency
        
    Returns:
        List[InternalTask]: List of tasks for the booking
    """
    logger.info(f"Getting tasks for booking {booking_id}")
    
    try:
        tasks = use_case.execute(booking_id=booking_id)
        logger.info(f"Retrieved {len(tasks)} tasks for booking {booking_id}")
        return tasks
    except Exception as e:
        logger.error(f"Unexpected error getting tasks: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.patch("/{task_id}/status", response_model=InternalTask)
async def update_task_status(
    booking_id: int = Path(..., gt=0, description="Booking ID"),
    task_id: int = Path(..., gt=0, description="Task ID"),
    status: str = ...,  # Will be extracted from request body
    use_case: UpdateTaskUseCase = Depends(get_update_task_use_case)
):
    """
    Update the status of a task.
    
    Args:
        booking_id: The booking identifier (path parameter)
        task_id: The task identifier (path parameter)
        status: The new status (request body)
        use_case: Update task use case dependency
        
    Returns:
        InternalTask: The updated task
        
    Raises:
        HTTPException: 404 if task not found, 400 for invalid status, 422 for validation errors
    """
    logger.info(f"Updating task {task_id} status to {status} for booking {booking_id}")
    
    try:
        task = use_case.execute(task_id=task_id, status=status)
        logger.info(f"Task {task_id} status updated to {status}")
        return task
    except ValueError as e:
        logger.warning(f"Failed to update task status: {str(e)}")
        if "not found" in str(e):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        elif "Invalid status" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e)
            )
    except Exception as e:
        logger.error(f"Unexpected error updating task status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )