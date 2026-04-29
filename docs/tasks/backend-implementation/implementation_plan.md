# Implementation Plan — backend-implementation

## 1. Technology Stack

*   **Framework:** FastAPI
*   **Package Manager:** uv
*   **Database:** SQLite
*   **ORM:** SQLAlchemy (async version with `asyncio`)
*   **Logging:** Loguru
*   **Testing:** Pytest
*   **Data Validation:** Pydantic (built into FastAPI)

## 2. Project Structure

```
/backend
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── tasks.py        # Endpoints for tasks
│   │   └── main.py             # FastAPI application entry point
│   │
│   ├── core/
│   │   ├── domain/
│   │   │   ├── __init__.py
│   │   │   └── models.py       # Models (entities), e.g., InternalTask
│   │   ├── interfaces/
│   │   │   ├── __init__.py
│   │   │   └── repositories.py # Abstract repositories (ITaskRepository)
│   │   └── use_cases/
│   │       ├── __init__.py
│   │       ├── create_task.py  # Use case for creating a task
│   │       ├── get_tasks.py    # Use case for getting tasks
│   │       └── update_task.py  # Use case for updating task status
│   │
│   └── infrastructure/
│       ├── __init__.py
│       ├── database/
│       │   ├── __init__.py
│       │   ├── database.py     # Database session setup (engine, sessionmaker)
│       │   ├── models.py       # SQLAlchemy models (tables)
│       │   └── repositories/
│       │       ├── __init__.py
│       │       └── tasks.py    # ITaskRepository implementation
│       └── logging.py          # Logging setup
│
├── tests/
        ├── __init__.py
        ├── conftest.py             # Common test fixtures
        ├── test_tasks.py           # Tests for task API
        ├── test_repositories.py    # Tests for repository layer
        ├── test_use_cases.py       # Tests for business logic (use cases)
        └── test_models.py          # Tests for Pydantic models
│
└── README.md
```

## 3. Step-by-Step Implementation Plan

### Step 1: Environment Setup and Basic Structure

1.  Create folder structure as described above.
2.  Initialize project with `uv`: create virtual environment (`uv venv`) and `pyproject.toml`/`requirements.txt` files.
3.  Install dependencies with `uv pip install`: FastAPI, Uvicorn, SQLAlchemy, Alembic, Pytest, Loguru.
4.  Create basic `.gitignore`.

### Step 2: Core Layer (Business Logic)

1.  **`core/domain/models.py`**:
    *   Define Pydantic model `InternalTask` with fields: `id`, `booking_id`, `title`, `status` (e.g., Enum: `OPEN`, `IN_PROGRESS`, `CLOSED`), `created_at`.

2.  **`core/interfaces/repositories.py`**:
    *   Create abstract class `ITaskRepository` with methods:
        *   `create(task: InternalTask) -> InternalTask`
        *   `get_by_booking_id(booking_id: int) -> list[InternalTask]`
        *   `get_by_id(task_id: int) -> InternalTask | None`
        *   `update_status(task_id: int, status: str) -> InternalTask`
        *   `exists(booking_id: int, title: str) -> bool` (for duplicate checks)

3.  **`core/use_cases/`**:
    *   **`create_task.py`**: Function/class that accepts `ITaskRepository` and task data. Logic: check for duplicate using `repository.exists()`, if no duplicate - create task via `repository.create()`.
    *   **`get_tasks.py`**: Function/class that accepts `ITaskRepository` and `booking_id`, returns list of tasks.
    *   **`update_task.py`**: Function/class that accepts `ITaskRepository`, `task_id` and `status`, updates task status.

### Step 3: Infrastructure Layer (Implementations)

1.  **`infrastructure/database/database.py`**:
    *   Setup `engine` and `sessionmaker` for async work with SQLite.
    *   Create function to get DB session (dependency).

2.  **`infrastructure/database/models.py`**:
    *   Define `InternalTaskTable` model using SQLAlchemy, corresponding to `InternalTask` domain model.

3.  **`infrastructure/database/repositories/tasks.py`**:
    *   Create `SQLAlchemyTaskRepository` class that inherits from `core.interfaces.repositories.ITaskRepository`.
    *   Implement all interface methods using SQLAlchemy session to interact with DB.

4.  **`infrastructure/logging.py`**:
    *   Setup `Loguru` logger. Can configure console output in `JSON` format for easy log parsing in the future.

### Step 4: Application Layer (FastAPI)

1.  **`app/main.py`**:
    *   Create FastAPI instance.
    *   Include router from `app/api/tasks.py`.
    *   Setup dependency injection for repository and import logging configuration.

2.  **`app/api/tasks.py`**:
    *   Create `APIRouter`.
    *   Define endpoints:
        *   `POST /bookings/{booking_id}/tasks`: Accepts data for task creation, uses `create_task` use case.
        *   `GET /bookings/{booking_id}/tasks`: Gets tasks, uses `get_tasks` use case.
        *   `PATCH /tasks/{task_id}/status`: Updates status, uses `update_task` use case.
    *   Use Pydantic schemas for input/output validation.

### Step 5: Testing

1.  **`tests/conftest.py`**:
    *   Create fixtures for:
        *   FastAPI test client (`TestClient`) with isolated application.
        *   In-memory SQLite database for tests with automatic table creation and deletion.
        *   Override repository dependency to test `TestTaskRepository`.
        *   Fixture for creating test data (seeding).
        *   Fixture for cleaning DB after each test.

2.  **`tests/test_tasks.py`**:
    *   Write tests for endpoints:
        *   `test_create_task_success`: Successful task creation (expect 201 Created).
        *   `test_create_task_duplicate_error`: Check duplicate creation prohibition (expect 409 Conflict).
        *   `test_get_tasks_empty`: Get empty task list for booking.
        *   `test_get_tasks_with_data`: Get task list with existing records.
        *   `test_get_tasks_wrong_booking`: Get tasks for non-existent booking (expect empty list).
        *   `test_update_task_status`: Successful status change (expect 200 OK).
        *   `test_update_task_status_invalid_transition`: Attempt incorrect status change (expect 400 Bad Request).
        *   `test_update_nonexistent_task`: Attempt to update non-existent task (expect 404 Not Found).
        *   `test_validation_error_empty_title`: Test for invalid input data - empty title (expect 422 Unprocessable Entity).
        *   `test_validation_error_invalid_status`: Test for invalid status (expect 422 Unprocessable Entity).
        *   `test_create_task_missing_booking_id`: Missing booking_id in path (expect 422 Unprocessable Entity).

3.  **`tests/test_repositories.py`**:
    *   Tests for repository layer:
        *   `test_create_and_retrieve_task`: Check task saving and reading.
        *   `test_exists_duplicate`: Check `exists` method for duplicates.
        *   `test_update_status_repository`: Check status change at DB level.
        *   `test_get_by_booking_id_empty`: Get tasks for booking without tasks.

4.  **`tests/test_use_cases.py`**:
    *   Tests for business logic (use cases) using mocks:
        *   `test_create_task_use_case_success`: Successful creation via use case.
        *   `test_create_task_use_case_duplicate`: Check duplicate via use case.
        *   `test_update_task_use_case_not_found`: Update non-existent task via use case.

5.  **`tests/test_models.py`**:
    *   Tests for Pydantic models:
        *   `test_internal_task_model_validation`: Check field validation.
        *   `test_internal_task_model_defaults`: Check default values.

6.  **`tests/conftest.py` - additional fixtures**:
    *   `sample_task_data()` - returns dictionary with valid data for task creation.
    *   `test_db_session()` - provides isolated DB session for each test.
    *   `task_repository()` - provides test repository.
    *   `api_client()` - provides FastAPI test client with overridden dependencies.

### Step 6: Logging and Monitoring (Description in README.md)

1.  **Logging (using Loguru)**:
    *   **Events**: `INFO` - task creation, status change. `WARNING` - attempt to create duplicate.
    *   **Errors**: `ERROR` - DB errors, unexpected exceptions.
2.  **Sentry**:
    *   Send all logs of level `ERROR` and above.
3.  **Grafana**:
    *   **Metrics**:
        *   `internal_task_created_total`: Counter of created tasks.
        *   `internal_task_active_count`: Number of active tasks (statuses `OPEN`, `IN_PROGRESS`).
        *   `internal_task_status_changed_total`: Counter of status changes with labels `from_status`, `to_status`.
        *   `internal_task_create_failed_total`: Counter of creation errors (duplicates, validation errors).
4.  **Alerts**:
    *   If `internal_task_create_failed_total` grows faster than N errors per 10 minutes — notify Tech Ops.
    *   If no tasks created (`internal_task_created_total`) in the last 24 hours (anomaly).

This plan ensures step-by-step development following clean architecture and SOLID principles, and covers all requirements from the TOR.
