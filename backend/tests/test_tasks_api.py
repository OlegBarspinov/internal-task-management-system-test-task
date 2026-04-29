"""
Tests for tasks API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from src.app.main import app
from src.core.domain.models import InternalTask, TaskStatus


def test_create_task_success(client):
    """Test successful task creation."""
    response = client.post(
        "/api/v1/bookings/1/tasks",
        json={"title": "Review contract"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Review contract"
    assert data["booking_id"] == 1
    assert data["status"] == TaskStatus.OPEN
    assert "id" in data
    assert "created_at" in data


def test_create_task_duplicate(client):
    """Test creating a duplicate task returns 409."""
    # First create a task
    client.post(
        "/api/v1/bookings/1/tasks",
        json={"title": "Review contract"}
    )
    # Try to create another with same title
    response = client.post(
        "/api/v1/bookings/1/tasks",
        json={"title": "Review contract"}
    )
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


def test_create_task_empty_title(client):
    """Test creating a task with empty title returns 422."""
    response = client.post(
        "/api/v1/bookings/1/tasks",
        json={"title": ""}
    )
    assert response.status_code == 422
    error_detail = response.json()["detail"]
    assert isinstance(error_detail, list)
    assert error_detail[0]["type"] == "string_too_short"
    assert error_detail[0]["loc"] == ["body", "title"]
    assert "String should have at least 1 character" in error_detail[0]["msg"]


def test_create_task_invalid_booking_id(client):
    """Test creating a task with invalid booking ID returns 422."""
    response = client.post(
        "/api/v1/bookings/0/tasks",  # booking_id must be > 0
        json={"title": "Review contract"}
    )
    assert response.status_code == 422


def test_get_tasks_success(client):
    """Test getting tasks for a booking with existing tasks."""
    # Create two tasks
    client.post("/api/v1/bookings/1/tasks", json={"title": "Task 1"})
    client.post("/api/v1/bookings/1/tasks", json={"title": "Task 2"})
    
    response = client.get("/api/v1/bookings/1/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"
    assert data[1]["title"] == "Task 2"


def test_get_tasks_empty(client):
    """Test getting tasks for a booking with no tasks returns empty list."""
    response = client.get("/api/v1/bookings/999/tasks")
    assert response.status_code == 200
    data = response.json()
    assert data == []


def test_get_tasks_invalid_booking_id(client):
    """Test getting tasks with invalid booking ID returns 422."""
    response = client.get("/api/v1/bookings/0/tasks")
    assert response.status_code == 422


def test_update_task_status_success(client):
    """Test successful task status update."""
    # Create a task
    create_response = client.post(
        "/api/v1/bookings/1/tasks",
        json={"title": "Review contract"}
    )
    task_id = create_response.json()["id"]
    
    # Update status
    response = client.patch(
        f"/api/v1/bookings/1/tasks/{task_id}/status",
        json={"status": "IN_PROGRESS"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["status"] == TaskStatus.IN_PROGRESS
    assert data["title"] == "Review contract"


def test_update_task_status_not_found(client):
    """Test updating status of non-existent task returns 404."""
    response = client.patch(
        "/api/v1/bookings/1/tasks/999/status",
        json={"status": "IN_PROGRESS"}
    )
    assert response.status_code == 404
    # The error message comes from the use case
    assert response.json()["detail"] == "Task with ID 999 not found"


def test_update_task_status_invalid_status(client):
    """Test updating task with invalid status returns 400."""
    # Create a task
    create_response = client.post(
        "/api/v1/bookings/1/tasks",
        json={"title": "Review contract"}
    )
    task_id = create_response.json()["id"]
    
    # Try to update with invalid status
    response = client.patch(
        f"/api/v1/bookings/1/tasks/{task_id}/status",
        json={"status": "INVALID_STATUS"}
    )
    assert response.status_code == 400
    assert "Invalid status" in response.json()["detail"]


def test_update_task_status_missing_status(client):
    """Test updating task with missing status returns 422."""
    # Create a task
    create_response = client.post(
        "/api/v1/bookings/1/tasks",
        json={"title": "Review contract"}
    )
    task_id = create_response.json()["id"]
    
    # Try to update without status field
    response = client.patch(
        f"/api/v1/bookings/1/tasks/{task_id}/status",
        json={}
    )
    assert response.status_code == 422