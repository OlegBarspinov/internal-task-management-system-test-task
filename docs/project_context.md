# Project Context & Architecture

## Project Overview
Backend implementation for internal task management system according to BACKEND_PLAN.md.

## Architecture
- **3-layer clean architecture** as specified in BACKEND_PLAN.md
- **Core Layer**: Domain models, interfaces, use cases (no external dependencies)
- **Application Layer**: FastAPI endpoints, thin I/O layer
- **Infrastructure Layer**: Database implementations, logging, external integrations

## Technology Stack
- **Framework**: FastAPI
- **Database**: SQLite with SQLAlchemy (async)
- **ORM**: SQLAlchemy with asyncio
- **Logging**: Loguru
- **Testing**: Pytest
- **Validation**: Pydantic (built-in FastAPI)

## Key Components
- **InternalTask**: Domain entity for task management
- **ITaskRepository**: Abstract interface for data access
- **Use Cases**: Business logic (create_task, get_tasks, update_task)
- **SQLAlchemyTaskRepository**: Concrete database implementation
- **FastAPI Endpoints**: REST API for task operations

## Dependencies Direction
```
Core Layer (no external dependencies)
    ↑
Application Layer (knows about Core)
    ↑
Infrastructure Layer (knows about all)
```

## Current State
- Project structure created: backend/src/
- Core layer initialization started
- Implementation in progress according to BACKEND_PLAN.md