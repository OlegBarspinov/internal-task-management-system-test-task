"""
Application layer.

Contains FastAPI application, API routes, and dependency injection configuration.
"""

from .main import app
from .exceptions import (
    AppException,
    app_exception_handler,
    integrity_error_handler,
    generic_exception_handler,
)
from .dependencies import (
    get_task_repository,
    get_create_task_use_case,
    get_get_tasks_use_case,
    get_update_task_use_case,
)
from .api import (
    CreateTaskRequest,
    UpdateTaskStatusRequest,
    TaskResponse,
    ApiResponse,
    ErrorResponse,
)

__all__ = [
    "app",
    "AppException",
    "app_exception_handler",
    "integrity_error_handler",
    "generic_exception_handler",
    "get_task_repository",
    "get_create_task_use_case",
    "get_get_tasks_use_case",
    "get_update_task_use_case",
    "CreateTaskRequest",
    "UpdateTaskStatusRequest",
    "TaskResponse",
    "ApiResponse",
    "ErrorResponse",
]
