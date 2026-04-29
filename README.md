# KeyGo Internal Task Management System

This project implements a mini backend and frontend for an internal task management service, focusing on handling tasks related to booking problems.

## Table of Contents

- [Project Context](#project-context)
- [Backend Setup and Run](#backend-setup-and-run)
- [Frontend Setup and Run](#frontend-setup-and-run)
- [Running Tests](#running-tests)
- [Implemented Features](#implemented-features)
- [Monitoring & Observability (Planned)](#monitoring--observability-planned)
- [Frontend README](frontend/README.md)


## Backend Setup and Run

The backend is built with **Python + FastAPI**. A virtual environment is assumed to be already set up in the repository.

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/OlegBarspinov/internal-task-management-system-test-task
   cd internal-task-management-system-test-task
   ```

2.  **Create virtual environment using UV** (optional but recommended)
    ```bash
    uv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    ```

3.  **Install dependencies from pyproject.toml using UV:**
    ```bash
    uv sync
    ```
    This installs all main dependencies (FastAPI, Uvicorn, SQLAlchemy, aiosqlite, loguru) and test dependencies (pytest, pytest-asyncio) from the pyproject.toml file using UV package manager.

4.  **Run the backend server:**
    ```bash
    uvicorn src.app.main:app
    ```
    The API will be available at `http://localhost:8000`. API documentation (Swagger UI) can be accessed at `http://localhost:8000/docs`.

## Frontend Setup and Run

The frontend is built with **React + Next.js**.

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install Node.js (if not already installed):**
    Node.js 18+ (20 LTS recommended) is required. Check your version:
    ```bash
    node --version
    npm --version
    ```

3.  **Install dependencies:**
    ```bash
    npm install
    ```

5.  **Run the frontend development server:**
    ```bash
    npm run dev
    ```
    The application will be available at `http://localhost:3000`.
    You can check its functionality by opening `http://localhost:3000/bookings/1` in your browser.

## Running Tests

### Backend Tests

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```
2.  **Activate the virtual environment** (if not already active).

4.  **Run all tests:**
    ```bash
    pytest
    ```

### Frontend Tests

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```
2.  **Run all tests:**
    ```bash
    npm test
    ```
    For coverage reports or watch mode, refer to the [Detailed Frontend Documentation](#detailed-frontend-documentation).

## Implemented Features

Based on the technical specification, the application implements:

*   **Backend API**:
    *   `InternalTask` entity.
    *   Endpoints for creating, retrieving, and updating the status of tasks.
*   **Frontend Page (`/bookings/[booking_id]`)**:
    *   Displays a list of internal tasks.
    *   Provides a form for creating new tasks.
    *   Allows changing the status of existing tasks.
*   **Tests**:
    *   Cover creation of tasks.
    *   Duplicate task prevention.
    *   Status change functionality.
    *   API error handling.

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
