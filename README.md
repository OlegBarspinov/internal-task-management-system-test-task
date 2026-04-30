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


## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/OlegBarspinov/internal-task-management-system-test-task
   cd internal-task-management-system-test-task
   ```

2.  **Create virtual environment using UV** (optional but recommended)
    ```bash
    uv venv
    source .venv/bin/activate  # Linux/Mac
    .venv\Scripts\activate     # Windows
    ```

3.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

4.  **Install dependencies from pyproject.toml using UV:**
    ```bash
    uv sync
    ```
    This installs all main dependencies (FastAPI, Uvicorn, SQLAlchemy, aiosqlite, loguru) and test dependencies (pytest, pytest-asyncio) from the pyproject.toml file using UV package manager.

5.  **Run the backend server (in /backend directory):**
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

### Logging

- **Events to Log:**
  - `INFO`: Task creation, status changes.
  - `WARNING`: Validation errors (e.g., duplicate task attempts).
  - `ERROR`: Unhandled exceptions, database errors.
  - `CRITICAL`: Application startup failures, critical service unavailability.


## Monitoring & Observability (Planned)

### Error Tracking (Sentry)

- **What to send to Sentry:**
  - All logs with level `ERROR` and `CRITICAL`. This includes unhandled exceptions, internal server errors, and failed database transactions.
- **How to connect:**
  - Integrate the Sentry SDK for Python. A FastAPI middleware would be used to automatically capture and report exceptions to Sentry.

### Metrics (Prometheus & Grafana)

- **Key Metrics to Expose:**
  - `internal_task_active_count`: Gauge of active tasks (status `OPEN` or `IN_PROGRESS`).
  - `internal_task_created_total`: Counter for every new task created.
  - `internal_task_status_changed_total`: Counter for task status changes, labeled by the new status.
  - `internal_task_create_failed_total`: Counter for failed task creation attempts.
  - `internal_task_creation_time_seconds`: Histogram of the time taken to create a task.
  - `http_requests_total`: Counter of HTTP requests, labeled by endpoint, method, and status code.
  - `http_requests_latency_seconds`: Histogram of request latency.
- **How to connect:**
  - The FastAPI application would expose a `/metrics` endpoint using a library like `prometheus-fastapi-instrumentator`.
  - Prometheus would be configured to scrape this endpoint.
  - Grafana would use Prometheus as a data source to build dashboards.

### Alerting (Alertmanager)

- **Alerts to Configure:**
  - **High Error Rate:** If `internal_task_create_failed_total` increases by more than N in 10 minutes, notify Tech Ops.
  - **High Latency:** If the 95th percentile of `internal_task_creation_time_seconds` exceeds X seconds, notify developers.
  - **API Failures:** If the rate of 5xx errors in `http_requests_total` is above Y for 5 minutes, notify the on-call engineer.
  - **System Inactivity:** If no new tasks are created in 24 hours, trigger a warning to check if the system is operating correctly.

