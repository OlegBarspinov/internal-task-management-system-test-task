"""
Database setup and session management.

Handles SQLAlchemy engine creation and session dependency for FastAPI.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
import os
from typing import AsyncGenerator

# Ensure all models are imported before initializing the base
from .models import Base, InternalTaskTable
from ..logging import logger # Corrected import path


# Database URL - using SQLite for simplicity
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite+aiosqlite:///./internal_tasks.db"
)

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    poolclass=NullPool,
)

# Create async session maker
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db():
    """
    Initializes the database by creating all tables defined in Base.metadata.
    """
    logger.info("Checking registered tables with SQLAlchemy...")
    logger.info(f"Tables in metadata: {list(Base.metadata.tables.keys())}")
    
    async with engine.begin() as conn:
        logger.info("Running create_all to generate database tables...")
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Tables should be created now.")


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a database session.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
