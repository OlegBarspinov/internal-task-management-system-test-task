"""
SQLAlchemy database models.

Defines the database table structures that correspond to domain entities.
"""

from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.orm import declarative_base
from datetime import datetime
from ...core.domain.models import TaskStatus


# Base class for all database models
Base = declarative_base()


class InternalTaskTable(Base):
    """
    SQLAlchemy model for internal tasks.
    
    Corresponds to the InternalTask domain entity.
    """
    
    __tablename__ = "internal_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    status = Column(SQLEnum(TaskStatus), nullable=False, default=TaskStatus.OPEN)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    __table_args__ = (
        UniqueConstraint('booking_id', 'title', name='uix_booking_title'),
    )
    
    def __repr__(self):
        return f"<InternalTaskTable(id={self.id}, booking_id={self.booking_id}, title='{self.title}', status='{self.status}')>"