"""
Task API endpoints.

Defines REST API endpoints for task management operations.
"""

from fastapi import APIRouter, Depends, HTTPException, Path, status, Body
from typing import List

from ...core.use_cases.create_task import CreateTaskUseCase
from ...core.use_cases.get_tasks import GetTasksUseCase
from ...core.use_cases.update_task import UpdateTaskUseCase
from ...core.domain.models import InternalTask, TaskStatus
from ...infrastructure.logging import logger
from ..dependencies import (
    get_create_task_use_case,
    get_get_tasks_use_case,
    get_update_task_use_case,
)
from .schemas import CreateTaskRequest, UpdateTaskStatusRequest

router = APIRouter(prefix="/bookings/{booking_id}/tasks", tags=["tasks"])


@router.post(
    "/",
    response_model=InternalTask,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new internal task associated with a booking. "
                "Task title must be unique per booking (case-sensitive)."
)
async def create_task(
    booking_id: int = Path(..., gt=0, description="Booking ID (must be positive integer)"),
    request: CreateTaskRequest = Body(..., examples=[{"title": "Review contract"}]),
    use_case: CreateTaskUseCase = Depends(get_create_task_use_case)
):
    """
    Create a new task for a booking.
    
    **Example request:**
    ```json
    {
        "title": "Review contract"
    }
    ```
    
    **Example response (201):**
    ```json
    {
        "id": 1,
        "booking_id": 1,
        "title": "Review contract",
        "status": "OPEN",
        "created_at": "2026-04-29T13:45:00"
    }
    ```
    
    **Error responses:**
    - `409 Conflict`: Task with this title already exists for this booking
    - `422 Unprocessable Entity`: Invalid request data (empty title, etc.)
    
    Args:
        booking_id: The booking identifier (path parameter)
        request: The task creation request body containing title
        use_case: Create task use case (injected by FastAPI)
        
    Returns:
        InternalTask: The created task with generated ID and timestamp
        
    Raises:
        HTTPException: 409 if duplicate, 422 for validation errors, 500 for unexpected errors
    """
    logger.info(f"Creating task for booking {booking_id}")
    
    try:
        task = await use_case.execute(booking_id=booking_id, title=request.title)
        logger.info(f"Task created successfully: id={task.id}, booking_id={booking_id}")
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


@router.get(
    "/",
    response_model=List[InternalTask],
    summary="Get all tasks for a booking",
    description="Retrieve a list of all tasks associated with a specific booking. "
                "Returns an empty list if no tasks exist for the booking."
)
async def get_tasks(
    booking_id: int = Path(..., gt=0, description="Booking ID (must be positive integer)"),
    use_case: GetTasksUseCase = Depends(get_get_tasks_use_case)
):
    """
    Get all tasks for a booking.
    
    **Example request:**
    `GET /api/v1/bookings/1/tasks`
    
    **Example response (200):**
    ```json
    [
        {
            "id": 1,
            "booking_id": 1,
            "title": "Review contract",
            "status": "OPEN",
            "created_at": "2026-04-29T13:45:00"
        },
        {
            "id": 2,
            "booking_id": 1,
            "title": "Schedule meeting",
            "status": "IN_PROGRESS",
            "created_at": "2026-04-29T14:00:00"
        }
    ]
    ```
    
    Args:
        booking_id: The booking identifier (path parameter)
        use_case: Get tasks use case (injected by FastAPI)
        
    Returns:
        List[InternalTask]: List of tasks for the booking (may be empty)
        
    Raises:
        HTTPException: 500 if unexpected error occurs
    """
    logger.info(f"Getting tasks for booking {booking_id}")
    
    try:
        tasks = await use_case.execute(booking_id=booking_id)
        logger.debug(f"Retrieved {len(tasks)} tasks for booking {booking_id}")
        return tasks
    except Exception as e:
        logger.error(f"Unexpected error getting tasks: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.patch(
    "/{task_id}/status",
    response_model=InternalTask,
    summary="Update task status",
    description="Update the status of an existing task. "
                "Valid statuses: OPEN, IN_PROGRESS, CLOSED."
)
async def update_task_status(
    booking_id: int = Path(..., gt=0, description="Booking ID (must be positive integer)"),
    task_id: int = Path(..., gt=0, description="Task ID (must be positive integer)"),
    request: UpdateTaskStatusRequest = Body(..., examples=[{"status": "IN_PROGRESS"}]),
    use_case: UpdateTaskUseCase = Depends(get_update_task_use_case)
):
    """
    Update the status of a task.
    
    **Example request:**
    ```json
    {
        "status": "IN_PROGRESS"
    }
    ```
    
    **Example response (200):**
    ```json
    {
        "id": 1,
        "booking_id": 1,
        "title": "Review contract",
        "status": "IN_PROGRESS",
        "created_at": "2026-04-29T13:45:00"
    }
    ```
    
    **Error responses:**
    - `404 Not Found`: Task with specified ID does not exist
    - `400 Bad Request`: Invalid status value (must be OPEN, IN_PROGRESS, or CLOSED)
    - `422 Unprocessable Entity`: Invalid request data
    
    Args:
        booking_id: The booking identifier (path parameter)
        task_id: The task identifier (path parameter)
        request: The status update request body containing new status
        use_case: Update task use case (injected by FastAPI)
        
    Returns:
        InternalTask: The updated task with new status
        
    Raises:
        HTTPException: 404 if not found, 400 for invalid status, 422 for validation errors, 500 for unexpected errors
    """
    logger.info(f"Updating task {task_id} status for booking {booking_id}")
    
    try:
        task = await use_case.execute(task_id=task_id, status=request.status)
        logger.info(f"Task {task_id} status updated to {request.status}")
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