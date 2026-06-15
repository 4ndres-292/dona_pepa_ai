"""Unit tests for the Doña Pepa API"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.models.user import User
from app.models.task import Task, TaskStatus, TaskPriority
from app.models.event import Event, EventType
from datetime import datetime, timedelta


# Use SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_db():
    """Clear database before each test"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


class TestHealth:
    """Health check tests"""
    
    def test_health_check(self):
        """Test health endpoint"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestUsers:
    """User endpoint tests"""
    
    def test_create_user(self):
        """Test creating a user"""
        response = client.post(
            "/api/v1/users",
            json={
                "name": "Test User",
                "email": "test@example.com",
                "bio": "Test bio"
            }
        )
        assert response.status_code == 201
        assert response.json()["name"] == "Test User"
        assert response.json()["email"] == "test@example.com"
    
    def test_create_duplicate_user(self):
        """Test creating duplicate user"""
        client.post(
            "/api/v1/users",
            json={"name": "User 1", "email": "test@example.com"}
        )
        response = client.post(
            "/api/v1/users",
            json={"name": "User 2", "email": "test@example.com"}
        )
        assert response.status_code == 400
    
    def test_list_users(self):
        """Test listing users"""
        client.post("/api/v1/users", json={"name": "User 1", "email": "user1@example.com"})
        client.post("/api/v1/users", json={"name": "User 2", "email": "user2@example.com"})
        
        response = client.get("/api/v1/users")
        assert response.status_code == 200
        assert len(response.json()) == 2
    
    def test_get_user(self):
        """Test getting a specific user"""
        response = client.post(
            "/api/v1/users",
            json={"name": "Test User", "email": "test@example.com"}
        )
        user_id = response.json()["id"]
        
        response = client.get(f"/api/v1/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Test User"
    
    def test_update_user(self):
        """Test updating a user"""
        response = client.post(
            "/api/v1/users",
            json={"name": "Test User", "email": "test@example.com"}
        )
        user_id = response.json()["id"]
        
        response = client.put(
            f"/api/v1/users/{user_id}",
            json={"name": "Updated User"}
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Updated User"


class TestTasks:
    """Task endpoint tests"""
    
    def test_create_task(self):
        """Test creating a task"""
        # Create user first
        user_response = client.post(
            "/api/v1/users",
            json={"name": "Test User", "email": "test@example.com"}
        )
        user_id = user_response.json()["id"]
        
        # Create task
        response = client.post(
            f"/api/v1/tasks?user_id={user_id}",
            json={
                "title": "Test Task",
                "description": "Test description",
                "priority": "high",
                "status": "pending"
            }
        )
        assert response.status_code == 201
        assert response.json()["title"] == "Test Task"
    
    def test_list_tasks(self):
        """Test listing tasks"""
        user_response = client.post(
            "/api/v1/users",
            json={"name": "Test User", "email": "test@example.com"}
        )
        user_id = user_response.json()["id"]
        
        # Create multiple tasks
        client.post(
            f"/api/v1/tasks?user_id={user_id}",
            json={"title": "Task 1", "priority": "high"}
        )
        client.post(
            f"/api/v1/tasks?user_id={user_id}",
            json={"title": "Task 2", "priority": "low"}
        )
        
        response = client.get(f"/api/v1/tasks?user_id={user_id}")
        assert response.status_code == 200
        assert len(response.json()) == 2


class TestEvents:
    """Event endpoint tests"""
    
    def test_create_event(self):
        """Test creating an event"""
        user_response = client.post(
            "/api/v1/users",
            json={"name": "Test User", "email": "test@example.com"}
        )
        user_id = user_response.json()["id"]
        
        now = datetime.utcnow()
        response = client.post(
            f"/api/v1/events?user_id={user_id}",
            json={
                "title": "Test Event",
                "event_type": "meeting",
                "start_time": now.isoformat(),
                "end_time": (now + timedelta(hours=1)).isoformat(),
                "location": "Test Location"
            }
        )
        assert response.status_code == 201
        assert response.json()["title"] == "Test Event"
