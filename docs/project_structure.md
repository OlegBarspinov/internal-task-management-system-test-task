# Project Structure

## Backend Structure (according to BACKEND_PLAN.md)

```
backend/
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── tasks.py        # Task endpoints
│   │   └── main.py             # FastAPI application entry point
│   │
│   ├── core/
│   │   ├── domain/
│   │   │   ├── __init__.py
│   │   │   └── models.py       # Domain entities (InternalTask)
│   │   ├── interfaces/
│   │   │   ├── __init__.py
│   │   │   └── repositories.py # Abstract repositories (ITaskRepository)
│   │   └── use_cases/
│   │       ├── __init__.py
│   │       ├── create_task.py  # Use case for task creation
│   │       ├── get_tasks.py    # Use case for getting tasks
│   │       └── update_task.py  # Use case for updating task status
│   │
│   └── infrastructure/
│       ├── __init__.py
│       ├── database/
│       │   ├── __init__.py
│       │   ├── database.py     # DB session setup (engine, sessionmaker)
│       │   ├── models.py       # SQLAlchemy models (tables)
│       │   └── repositories/
│       │       ├── __init__.py
│       │       └── tasks.py    # ITaskRepository implementation
│       └── logging.py          # Loguru configuration
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Common test fixtures
│   ├── test_tasks.py           # API tests
│   ├── test_repositories.py    # Repository layer tests
│   ├── test_use_cases.py       # Business logic tests
│   └── test_models.py          # Pydantic model tests
│
└── README.md
```

## Architecture Layers

### Core Layer (`src/core/`)
- Pure Python, no external dependencies
- Domain entities, business logic
- Abstract interfaces (ports)
- Use cases (business operations)

### Application Layer (`src/app/`)
- FastAPI endpoints
- Thin I/O layer
- Input validation (Pydantic)
- Response formatting

### Infrastructure Layer (`src/infrastructure/`)
- Concrete implementations
- Database (SQLAlchemy)
- External APIs
- Logging (Loguru)