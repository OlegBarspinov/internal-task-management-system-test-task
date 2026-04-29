# Project Context & Architecture

## Project Overview
Backend implementation for internal task management system according to BACKEND_PLAN.md.
Provides REST API for managing tasks associated with bookings.

## Architecture (Clean Architecture / Hexagonal)
```
┌─────────────────────────────────────────────────────────────┐
│                    Infrastructure Layer                     │
│  (Database: SQLAlchemy, Logging: Loguru, External APIs)    │
├─────────────────────────────────────────────────────────────┤
│                Application Layer (FastAPI)                  │
│  (Endpoints, DTOs, Dependency Injection, Exception Handling)│
├─────────────────────────────────────────────────────────────┤
│                    Core Layer (Domain)                      │
│  (Entities, Use Cases, Repository Interfaces)              │
└─────────────────────────────────────────────────────────────┘
```

### Core Layer (`src/core/`)
- **Pure Python**, no external dependencies
- Domain entities: `InternalTask`, `TaskStatus` (enum)
- Abstract interfaces: `ITaskRepository` (port)
- Use cases (business operations):
  - `CreateTaskUseCase`
  - `GetTasksUseCase`
  - `UpdateTaskUseCase`
- Validation: business rules (duplicate detection, status validation)

### Application Layer (`src/app/`)
- **FastAPI** application (`main.py`) with CORS, lifespan, routing
- **Exception handling** (`exceptions.py`):
  - `AppException` base class
  - `DuplicateTaskError`, `TaskNotFoundError`, `InvalidStatusError`
  - Global handlers for 409, 404, 400, 500 responses
  - Structured error responses with `ErrorResponse` schema
- **Dependency Injection** (`dependencies.py`):
  - `get_task_repository()`
  - `get_create_task_use_case()`
  - `get_get_tasks_use_case()`
  - `get_update_task_use_case()`
- **API endpoints** (`api/`):
  - `basic.py` - `/` (info), `/health` (health check)
  - `tasks.py` - CRUD operations for tasks with comprehensive docstrings
- **Schemas** (`api/schemas.py`):
  - Request: `CreateTaskRequest`, `UpdateTaskStatusRequest`
  - Response: `TaskResponse`, `ApiResponse[T]`, `ErrorResponse`
  - All schemas use Pydantic v2 with `from_attributes=True` for ORM compatibility

### Infrastructure Layer (`src/infrastructure/`)
- **Database** (`database/`):
  - `database.py` - async engine, session factory, `get_db_session` dependency
  - `models.py` - `InternalTaskTable` (SQLAlchemy), `Base` declarative
  - `repositories/tasks.py` - `SQLAlchemyTaskRepository` implements `ITaskRepository`
- **Logging** (`logging.py`) - Loguru configured with console + file output

## Technology Stack
- **Framework**: FastAPI 0.104.1
- **Database**: SQLite (aiosqlite) - async driver
- **ORM**: SQLAlchemy 2.0.23 (async mode)
- **Logging**: Loguru 0.7.2
- **Validation**: Pydantic (integrated in FastAPI)
- **Testing**: Pytest 7.4.3, pytest-asyncio 0.23.6
- **Package**: Python 3.11+

## Dependencies Direction (Strict)
```
Core Layer (no external dependencies)
    ↑
Application Layer (knows about Core only)
    ↑
Infrastructure Layer (implements Core interfaces)
```
**Rule**: Inner layers must not depend on outer layers. Infrastructure implements Core interfaces.

## Key Design Patterns
- **Repository Pattern**: Data access abstracted via `ITaskRepository`
- **Use Case Pattern**: Each business operation is a separate use case class
- **Dependency Injection**: FastAPI `Depends` for all dependencies
- **Single Responsibility**: Each class/file has one clear purpose
- **Async/Await**: All I/O operations are asynchronous


## API Endpoints
| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/` | API info | ✅ |
| GET | `/health` | Health check | ✅ |
| POST | `/api/v1/bookings/{booking_id}/tasks` | Create task | ✅ |
| GET | `/api/v1/bookings/{booking_id}/tasks` | List tasks | ✅ |
| PATCH | `/api/v1/tasks/{task_id}/status` | Update status | ✅ |

## Error Handling
- **400** - Invalid status value
- **404** - Task not found
- **409** - Duplicate task (unique constraint violation)
- **422** - Validation error (Pydantic)
- **500** - Unexpected server error

#