"""User schemas"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


class UserBase(BaseModel):
    """Base user schema"""
    name: str
    email: EmailStr
    bio: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a user"""
    pass


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserDetailResponse(UserResponse):
    """Detailed user response with related data"""
    tasks: List["TaskResponseBase"] = []
    events: List["EventResponseBase"] = []
    
    class Config:
        from_attributes = True


# Import forward references
from app.schemas.task import TaskResponseBase
from app.schemas.event import EventResponseBase
