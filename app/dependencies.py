"""Dependency injection"""
from sqlalchemy.orm import Session
from fastapi import Depends

from app.database import get_db
from app.config import get_settings


def get_current_db() -> Session:
    """Get current database session"""
    return Depends(get_db)


def get_current_settings():
    """Get current settings"""
    return Depends(get_settings)
