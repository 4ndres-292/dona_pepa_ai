"""Database test and initialization utilities"""
import os
from app.database import engine, Base, SessionLocal
from app.models.user import User
from app.models.task import Task, TaskStatus, TaskPriority
from app.models.event import Event, EventType
from datetime import datetime, timedelta


def init_db():
    """Initialize database with tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully")


def seed_db():
    """Seed database with sample data"""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(User).first():
            print("✓ Database already contains data, skipping seed")
            return
        
        # Create sample users
        users = [
            User(name="Juan García", email="juan@example.com", bio="Productivity enthusiast"),
            User(name="María López", email="maria@example.com", bio="AI researcher"),
            User(name="Carlos Rodríguez", email="carlos@example.com", bio="Developer"),
        ]
        
        db.add_all(users)
        db.flush()  # Get user IDs
        
        # Create sample tasks
        now = datetime.utcnow()
        tasks = [
            Task(
                user_id=users[0].id,
                title="Complete project documentation",
                description="Write comprehensive docs for Doña Pepa",
                status=TaskStatus.IN_PROGRESS,
                priority=TaskPriority.HIGH,
                deadline=now + timedelta(days=7),
            ),
            Task(
                user_id=users[0].id,
                title="Review code pull requests",
                description="Review and approve pending PRs",
                status=TaskStatus.PENDING,
                priority=TaskPriority.MEDIUM,
                deadline=now + timedelta(days=3),
            ),
            Task(
                user_id=users[1].id,
                title="Research AI models",
                description="Evaluate new language models for integration",
                status=TaskStatus.PENDING,
                priority=TaskPriority.HIGH,
                deadline=now + timedelta(days=14),
            ),
            Task(
                user_id=users[2].id,
                title="Fix authentication bug",
                description="Debug JWT token validation issue",
                status=TaskStatus.IN_PROGRESS,
                priority=TaskPriority.URGENT,
                deadline=now + timedelta(days=1),
            ),
        ]
        
        db.add_all(tasks)
        db.flush()
        
        # Create sample events
        events = [
            Event(
                user_id=users[0].id,
                title="Team standup",
                event_type=EventType.MEETING,
                start_time=now + timedelta(days=1, hours=9),
                end_time=now + timedelta(days=1, hours=10),
                location="Conference Room A",
            ),
            Event(
                user_id=users[0].id,
                title="Project deadline",
                event_type=EventType.DEADLINE,
                start_time=now + timedelta(days=7),
                end_time=now + timedelta(days=7, hours=23, minutes=59),
                is_all_day=True,
            ),
            Event(
                user_id=users[1].id,
                title="Conference talk",
                event_type=EventType.WORK,
                start_time=now + timedelta(days=30, hours=14),
                end_time=now + timedelta(days=30, hours=15, minutes=30),
                location="Virtual - Zoom",
            ),
            Event(
                user_id=users[2].id,
                title="1:1 with manager",
                event_type=EventType.MEETING,
                start_time=now + timedelta(days=2, hours=15),
                end_time=now + timedelta(days=2, hours=16),
                location="Manager's office",
            ),
        ]
        
        db.add_all(events)
        db.commit()
        
        print("✓ Database seeded with sample data")
        print(f"  - Created {len(users)} users")
        print(f"  - Created {len(tasks)} tasks")
        print(f"  - Created {len(events)} events")
        
    finally:
        db.close()


def clear_db():
    """Clear all database tables"""
    print("Clearing database...")
    Base.metadata.drop_all(bind=engine)
    print("✓ Database cleared successfully")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "init":
            init_db()
        elif command == "seed":
            init_db()
            seed_db()
        elif command == "clear":
            clear_db()
        elif command == "reset":
            clear_db()
            init_db()
            seed_db()
        else:
            print(f"Unknown command: {command}")
            print("Available commands: init, seed, clear, reset")
    else:
        print("Database utilities for Doña Pepa")
        print("Usage: python db_init.py [init|seed|clear|reset]")
        print("  init  - Create database tables")
        print("  seed  - Create tables and seed with sample data")
        print("  clear - Drop all tables")
        print("  reset - Drop tables and recreate with sample data")
