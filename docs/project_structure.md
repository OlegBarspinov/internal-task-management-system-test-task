# Project Structure

## Backend Structure

```
backend/
├── src/
│   ├── app/
│   │   ├── __init__.py          # Application package exports
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── exceptions.py        # Custom exception classes & handlers
│   │   ├── dependencies.py      # Dependency injection configuration
│   │   ├── api/
│   │   │   ├── __init__.py      # API package exports
│   │   │   ├── basic.py         # Basic endpoints (/, /health)
│   │   │   ├── tasks.py         # Task endpoints (CRUD)
│   │   │   └── schemas.py       # Pydantic request/response models
│   │   │                       # - Request: CreateTaskRequest, UpdateTaskStatusRequest
│   │   │                       # - Response: TaskResponse, ApiResponse[T], ErrorResponse
│   │   └── ...
│   │
│   ├── core/
│   │   ├── __init__.py          # Core package exports
│   │   ├── domain/
│   │   │   ├── __init__.py
│   │   │   └── models.py        # Domain entities (InternalTask, TaskStatus)
│   │   ├── interfaces/
│   │   │   ├── __init__.py
│   │   │   └── repositories.py  # Abstract repository interfaces (ITaskRepository)
│   │   └── use_cases/
│   │       ├── __init__.py
│   │       ├── create_task.py   # Use case for task creation (async)
│   │       ├── get_tasks.py     # Use case for getting tasks (async)
│   │       └── update_task.py   # Use case for updating task status (async)
│   │
│   └── infrastructure/
│       ├── __init__.py          # Infrastructure package exports
│       ├── logging.py           # Loguru configuration (no sensitive data in logs)
│       └── database/
│           ├── __init__.py
│           ├── database.py      # DB session setup (async engine, sessionmaker)
│           ├── models.py        # SQLAlchemy models (InternalTaskTable with constraints)
│           └── repositories/
│               ├── __init__.py
│               └── tasks.py     # ITaskRepository implementation (SQLAlchemy, async)
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Common test fixtures (async engine with StaticPool)
│   ├── test_tasks.py            # API endpoint tests (with 500 error test)
│   ├── test_repositories.py     # Repository layer tests
│   ├── test_use_cases.py        # Business logic unit tests (with mocks)
│   └── test_models.py           # Domain model tests
│
├── pyproject.toml               # Project configuration & dependencies (asyncio_mode=auto)
├── .gitignore                   # Git ignore rules (Python, IDE, logs, cache)
└── README.md                    # Project documentation
```

