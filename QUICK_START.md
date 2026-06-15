# Quick Start Guide - Doña Pepa FastAPI Backend

## 5-Minute Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Database
Create `.env` file:
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/dona_pepa
```

### 3. Initialize Database
```bash
python db_init.py seed
```

### 4. Run Server
```bash
python main.py
```

Visit: `http://localhost:8000`

---

## Quick API Test

### Create a User
```bash
curl -X POST "http://localhost:8000/api/v1/users" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "bio": "Productivity enthusiast"
  }'
```

### Create a Task
```bash
# Replace user_id with actual ID from previous response
curl -X POST "http://localhost:8000/api/v1/tasks?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn FastAPI",
    "description": "Master FastAPI fundamentals",
    "priority": "high",
    "status": "in_progress"
  }'
```

### Create an Event
```bash
curl -X POST "http://localhost:8000/api/v1/events?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Team Meeting",
    "event_type": "meeting",
    "start_time": "2026-06-20T10:00:00",
    "end_time": "2026-06-20T11:00:00",
    "location": "Conference Room A"
  }'
```

### View Interactive Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Database Commands

```bash
# Initialize empty database
python db_init.py init

# Seed with sample data
python db_init.py seed

# Reset everything
python db_init.py reset

# Clear all data
python db_init.py clear
```

---

## Running Tests

```bash
pip install pytest pytest-asyncio httpx
pytest test_api.py -v
```

---

## Project Structure Overview

```
app/
├── main.py          → FastAPI app creation
├── config.py        → Settings management
├── database.py      → Database connection
├── models/          → SQLAlchemy models
├── schemas/         → Pydantic validation schemas
└── routes/          → API endpoint definitions
```

---

## Common Tasks

### Change Server Port
```bash
# Edit main.py line:
uvicorn.run(..., port=8001, ...)
```

### Enable Debug Logging
```bash
# In .env:
LOG_LEVEL=DEBUG
```

### Access Database Directly
```python
from app.database import SessionLocal
db = SessionLocal()
# Use db.query(Model) to interact directly
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `Connection refused` | Ensure PostgreSQL is running |
| `Port 8000 in use` | Use different port: `python main.py --port 8001` |
| `Table already exists` | Run `python db_init.py reset` |
| `Import errors` | Reinstall: `pip install -r requirements.txt --force-reinstall` |

---

## Next Steps

1. ✅ API running
2. 📚 Read [BACKEND_SETUP.md](BACKEND_SETUP.md) for detailed documentation
3. 🧪 Explore `/docs` for interactive API testing
4. 🔐 Add authentication (see Future Enhancements)
5. 📊 Add advanced queries and filtering
6. 🚀 Deploy to production

---

## API Endpoints Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/health` | Check API status |
| POST | `/api/v1/users` | Create user |
| GET | `/api/v1/users` | List users |
| GET | `/api/v1/users/{id}` | Get user details |
| PUT | `/api/v1/users/{id}` | Update user |
| DELETE | `/api/v1/users/{id}` | Delete user |
| POST | `/api/v1/tasks?user_id=X` | Create task |
| GET | `/api/v1/tasks?user_id=X` | List tasks |
| GET | `/api/v1/tasks/{id}` | Get task |
| PUT | `/api/v1/tasks/{id}` | Update task |
| DELETE | `/api/v1/tasks/{id}` | Delete task |
| POST | `/api/v1/events?user_id=X` | Create event |
| GET | `/api/v1/events?user_id=X` | List events |
| GET | `/api/v1/events/{id}` | Get event |
| PUT | `/api/v1/events/{id}` | Update event |
| DELETE | `/api/v1/events/{id}` | Delete event |

---

**Happy coding! 🚀**
