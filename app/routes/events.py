"""Event routes"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models.event import Event
from app.models.user import User
from app.schemas.event import EventCreate, EventUpdate, EventResponse

router = APIRouter(prefix="/api/v1/events", tags=["events"])


@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(event: EventCreate, user_id: int = Query(...), db: Session = Depends(get_db)) -> EventResponse:
    """
    Create a new event
    
    Args:
        event: Event data to create
        user_id: User ID
        db: Database session
        
    Returns:
        EventResponse: Created event
    """
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Validate start_time < end_time
    if event.start_time >= event.end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start time must be before end time"
        )
    
    db_event = Event(user_id=user_id, **event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


@router.get("", response_model=List[EventResponse])
def list_events(
    user_id: int = Query(...),
    start_date: datetime = Query(None),
    end_date: datetime = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> List[EventResponse]:
    """
    List events for a user
    
    Args:
        user_id: User ID
        start_date: Filter events after this date
        end_date: Filter events before this date
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List[EventResponse]: List of events
    """
    query = db.query(Event).filter(Event.user_id == user_id)
    
    if start_date:
        query = query.filter(Event.start_time >= start_date)
    
    if end_date:
        query = query.filter(Event.end_time <= end_date)
    
    events = query.offset(skip).limit(limit).all()
    return events


@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)) -> EventResponse:
    """
    Get event by ID
    
    Args:
        event_id: Event ID
        db: Database session
        
    Returns:
        EventResponse: Event details
    """
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return event


@router.put("/{event_id}", response_model=EventResponse)
def update_event(event_id: int, event_update: EventUpdate, db: Session = Depends(get_db)) -> EventResponse:
    """
    Update an event
    
    Args:
        event_id: Event ID
        event_update: Event data to update
        db: Database session
        
    Returns:
        EventResponse: Updated event
    """
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    update_data = event_update.model_dump(exclude_unset=True)
    
    # Validate start_time < end_time if both are being updated
    if "start_time" in update_data and "end_time" in update_data:
        if update_data["start_time"] >= update_data["end_time"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Start time must be before end time"
            )
    
    for key, value in update_data.items():
        setattr(db_event, key, value)
    
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, db: Session = Depends(get_db)) -> None:
    """
    Delete an event
    
    Args:
        event_id: Event ID
        db: Database session
    """
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    db.delete(db_event)
    db.commit()
