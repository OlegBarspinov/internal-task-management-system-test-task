# Internal Task Management System

Backend API for managing internal tasks related to bookings, built with FastAPI following clean architecture principles.

## Overview

This system provides a REST API for creating, retrieving, and updating internal tasks associated with bookings. It implements duplicate prevention, status tracking, and comprehensive logging.

## Features

- **Task Management**: Create, retrieve, and update tasks
- **Duplicate Prevention**: Prevents creation of tasks with same booking_id and title
- **Status Tracking**: Tasks can be OPEN, IN_PROGRESS, or CLOSED
- **RESTful API**: Standard HTTP endpoints with JSON responses
- **Clean Architecture**: Separation of concerns (Core, Application, Infrastructure)
- **Comprehensive Testing**: Unit and integration tests with pytest
- **Logging**: Structured logging with Loguru
- **Validation**: Input validation with Pydantic

## Technology Stack

- **Framework**: FastAPI
- **Language**: Python 3.8+
- **Database**: SQLite with SQLAlchemy (async)
- **ORM**: SQLAlchemy 2.0
- **Validation**: Pydantic
- **Logging**: Loguru
- **Testing**: Pytest, pytest-asyncio
- **API Docs**: Swagger UI (automatically generated)

## Project Structure

```
backend/
├── src/
│   ├── app/                 # Application layer (FastAPI)
│   │   ├── api/             # API endpoints
│   │   └── main.py          # App entry point
│   │
│   ├── core/                # Core layer (business logic)
│   │   ├── domain/          # Domain entities
│   │   ├── interfaces/      # Abstract interfaces
│   │   └── use_cases/       # Business operations
│   │
│   └── infrastructure/      # Infrastructure layer
│       ├── database/        # Database implementations
│       └── logging.py       # Logging configuration
│
├── tests/                   # Test suite
│   ├── conftest.py          # Test fixtures
│   ├── test_tasks.py        # API tests
│   ├── test_repositories.py # Repository tests
│   ├── test_use_cases.py    # Use case tests
│   └── test_models.py       # Model tests
│
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Project configuration
└── .gitignore              # Git ignore rules
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Create virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

## Running the Application

1. **Start the server**
   ```bash
   cd backend
   uvicorn src.app.main:app --reload
   ```

2. **Access the API**
   - Base URL: `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`
   - Alternative Docs: `http://localhost:8000/redoc`

## API Endpoints

### Create Task
```
POST /bookings/{booking_id}/tasks
```
Create a new task for a booking.

**Parameters:**
- `booking_id` (path): Booking identifier (integer > 0)
- `title` (body): Task title (string, required)

**Response:**
- `201 Created`: Task created successfully
- `409 Conflict`: Duplicate task exists
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Unexpected error

### Get Tasks
```
GET /bookings/{booking_id}/tasks
```
Retrieve all tasks for a booking.

**Parameters:**
- `booking_id` (path): Booking identifier (integer > 0)

**Response:**
- `200 OK`: List of tasks (may be empty)
- `500 Internal Server Error`: Unexpected error

### Update Task Status
```
PATCH /tasks/{task_id}/status
```
Update the status of a task.

**Parameters:**
- `task_id` (path): Task identifier (integer > 0)
- `status` (body): New status (string: OPEN, IN_PROGRESS, CLOSED)

**Response:**
- `200 OK`: Task updated successfully
- `400 Bad Request`: Invalid status value
- `404 Not Found`: Task not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Unexpected error

## Running Tests

1. **Install test dependencies**
   ```bash
   pip install -r backend/requirements.txt
   pip install pytest pytest-asyncio
   ```

2. **Run all tests**
   ```bash
   cd backend
   pytest
   ```

3. **Run tests with coverage**
   ```bash
   pytest --cov=src --cov-report=html
   ```

## Logging

The application uses Loguru for structured logging. Logs are output to:
- Console (colored, formatted output)
- File (`logs/app.log`) with rotation and retention

Log levels:
- `INFO`: General application events
- `WARNING`: Potential issues (e.g., duplicate task attempts)
- `ERROR`: Errors and exceptions
- `DEBUG`: Detailed debugging information

## Monitoring & Observability (Planned)

As mentioned in the requirements, the following would be implemented for production:

### Metrics (for Grafana/Prometheus)
- `internal_task_created_total`: Counter of created tasks
- `internal_task_active_count`: Gauge of active tasks (OPEN, IN_PROGRESS)
- `internal_task_status_changed_total`: Counter of status changes
- `internal_task_create_failed_total`: Counter of failed creation attempts

### Alerts
- Rapid increase in failed task creation (> N errors/10 min)
- No task creation in 24 hours (potential system issue)

### Error Tracking
- Sentry integration for ERROR level logs and above

## Clean Architecture Layers

### Core Layer (`src/core/`)
- **Domain Entities**: Pure Python/Pydantic models with business logic
- **Interfaces**: Abstract repositories defining contracts
- **Use Cases**: Business operations coordinating entities and interfaces
- **Dependencies**: None on external frameworks

### Application Layer (`src/app/`)
- **FastAPI App**: Application setup and middleware
- **API Endpoints**: REST controllers with dependency injection
- **Dependencies**: Core layer only

### Infrastructure Layer (`src/infrastructure/`)
- **Database**: SQLAlchemy implementations of repositories
- **Logging**: Loguru configuration
- **Dependencies**: All layers and external libraries

## Design Principles

1. **Single Responsibility**: Each class/function has one clear purpose
2. **Open/Closed**: Open for extension, closed for modification
3. **Liskov Substitution**: Implementations can be swapped without breaking
4. **Interface Segregation**: Small, focused interfaces
5. **Dependency Inversion**: Depend on abstractions, not concretions
6. **Clean Code**: Readable, maintainable, well-documented code
7. **Testing**: High test coverage for critical paths

## License

MIT License - see LICENSE file for details.