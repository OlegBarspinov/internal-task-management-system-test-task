"""
Test configuration and fixtures.

Provides common fixtures for testing the application including:
- Test database setup
- Test client for FastAPI
- Repository overrides
- Sample data
"""

import asyncio
import pytest
from typing import AsyncGenerator, Generator
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool

from src.app.main import app
from src.infrastructure.database.database import get_db_session, AsyncSessionLocal
from src.infrastructure.database.models import Base
from src.infrastructure.database.repositories.tasks import SQLAlchemyTaskRepository
from src.core.use_cases.create_task import CreateTaskUseCase
from src.core.use_cases.get_tasks import GetTasksUseCase
from src.core.use_cases.update_task import UpdateTaskUseCase


# Test database URL - using in-memory SQLite for tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_engine():
    """Create test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        future=True,
        poolclass=NullPool,
    )
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Drop tables after tests
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest.fixture
async def test_db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session."""
    test_async_session_local = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with test_async_session_local() as session:
        yield session
        await session.rollback()


@pytest.fixture
def client(test_db_session) -> TestClient:
    """Create test client with overridden dependencies."""
    
    async def override_get_db_session() -> AsyncGenerator[AsyncSession, None]:
        yield test_db_session
    
    app.dependency_overrides[get_db_session] = override_get_db_session
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def test_task_repository(test_db_session) -> SQLAlchemyTaskRepository:
    """Create test task repository."""
    return SQLAlchemyTaskRepository(test_db_session)


@pytest.fixture
def test_create_task_use_case(test_task_repository) -> CreateTaskUseCase:
    """Create test create task use case."""
    return CreateTaskUseCase(test_task_repository)


@pytest.fixture
def test_get_tasks_use_case(test_task_repository) -> GetTasksUseCase:
    """Create test get tasks use case."""
    return GetTasksUseCase(test_task_repository)


@pytest.fixture
def test_update_task_use_case(test_task_repository) -> UpdateTaskUseCase:
    """Create test update task use case."""
    return UpdateTaskUseCase(test_task_repository)


@pytest.fixture
def sample_task_data():
    """Sample task data for testing."""
    return {
        "booking_id": 1,
        "title": "Test task title"
    }