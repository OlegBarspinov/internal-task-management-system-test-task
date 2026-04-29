"""
Application dependencies.

Provides dependency injection for FastAPI endpoints.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..infrastructure.database.repositories.tasks import SQLAlchemyTaskRepository
from ..infrastructure.database.database import get_db_session
from ..core.use_cases.create_task import CreateTaskUseCase
from ..core.use_cases.get_tasks import GetTasksUseCase
from ..core.use_cases.update_task import UpdateTaskUseCase


def get_task_repository(
    db: AsyncSession = Depends(get_db_session)
) -> SQLAlchemyTaskRepository:
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
