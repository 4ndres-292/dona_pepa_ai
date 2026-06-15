"""Event model"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.database import Base


class EventType(str, enum.Enum):
    """Event type enumeration"""
    MEETING = "meeting"
    DEADLINE = "deadline"
    REMINDER = "reminder"
    PERSONAL = "personal"
    WORK = "work"
    SOCIAL = "social"


class Event(Base):
    """Event model for managing calendar events"""
    
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    event_type = Column(Enum(EventType), default=EventType.PERSONAL, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    location = Column(String(255), nullable=True)
    is_all_day = Column(Boolean, default=False, nullable=False)
    is_recurring = Column(Boolean, default=False, nullable=False)
    recurrence_pattern = Column(String(50), nullable=True)  # daily, weekly, monthly
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="events")
    
    def __repr__(self) -> str:
        return f"<Event(id={self.id}, title={self.title}, start_time={self.start_time})>"
