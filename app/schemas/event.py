"""Event schemas"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


class EventType(str, Enum):
    """Event type"""
    MEETING = "meeting"
    DEADLINE = "deadline"
    REMINDER = "reminder"
    PERSONAL = "personal"
    WORK = "work"
    SOCIAL = "social"


class EventBase(BaseModel):
    """Base event schema"""
    title: str
    description: Optional[str] = None
    event_type: EventType = EventType.PERSONAL
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    is_all_day: bool = False
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None


class EventCreate(EventBase):
    """Schema for creating an event"""
    pass


class EventUpdate(BaseModel):
    """Schema for updating an event"""
    title: Optional[str] = None
    description: Optional[str] = None
    event_type: Optional[EventType] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    is_all_day: Optional[bool] = None
    is_recurring: Optional[bool] = None
    recurrence_pattern: Optional[str] = None


class EventResponseBase(EventBase):
    """Base event response schema"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class EventResponse(EventResponseBase):
    """Event response schema"""
    pass
