# FastAPI Backend - Doña Pepa

Complete FastAPI backend implementation for the Doña Pepa AI productivity assistant.

## Project Structure

```
dona_pepa_ai/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application factory
│   ├── config.py               # Configuration settings
│   ├── database.py             # Database setup and session management
│   ├── dependencies.py         # Dependency injection
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py            # User model
│   │   ├── task.py            # Task model
│   │   └── event.py           # Event model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py            # User Pydantic schemas
│   │   ├── task.py            # Task Pydantic schemas
│   │   └── event.py           # Event Pydantic schemas
│   └── routes/
│       ├── __init__.py
│       ├── health.py          # Health check endpoint
│       ├── users.py           # User routes
│       ├── tasks.py           # Task routes
│       └── events.py          # Event routes
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── .env.example                # Environment variables template
└── schema.sql                  # SQL schema reference
```

## Features

### User Management
- Create, read, update, delete users
- Email-based user identification
- User profile with bio
- Relationship management with tasks and events

### Task Management
- Task CRUD operations
- Task statuses: pending, in_progress, completed, cancelled
- Task priorities: low, medium, high, urgent
- Support for recurring tasks
- Deadline tracking
- Completion tracking

### Event Management
- Event CRUD operations
- Multiple event types: meeting, deadline, reminder, personal, work, social
- Date/time range support
- All-day event support
- Location tracking
- Recurring event support

### API Features
- Health check endpoint
- RESTful API design
- Comprehensive error handling
- Data validation with Pydantic
- CORS support
- Database session management
- Automatic table creation on startup

## Installation

### Prerequisites
- Python 3.10+
- PostgreSQL 12+
- pip or poetry

### Setup Steps

1. **Clone the repository**
```bash
cd d:\Proyectos\Copilot\dona_pepa_ai
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# or
source venv/bin/activate  # On macOS/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
copy .env.example .env
# Edit .env with your PostgreSQL configuration
```

Example `.env`:
```
DATABASE_URL=postgresql://username:password@localhost:5432/dona_pepa
API_TITLE=Doña Pepa API
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

5. **Create PostgreSQL database**
```sql
CREATE DATABASE dona_pepa;
```

6. **Run the application**
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
- `GET /api/v1/health` - Check API health status

### Users
- `POST /api/v1/users` - Create a new user
- `GET /api/v1/users` - List all users (with pagination)
- `GET /api/v1/users/{user_id}` - Get user details with tasks and events
- `PUT /api/v1/users/{user_id}` - Update user information
- `DELETE /api/v1/users/{user_id}` - Delete a user

### Tasks
- `POST /api/v1/tasks?user_id={user_id}` - Create a new task
- `GET /api/v1/tasks?user_id={user_id}` - List tasks for a user (with filtering)
- `GET /api/v1/tasks/{task_id}` - Get task details
- `PUT /api/v1/tasks/{task_id}` - Update task
- `DELETE /api/v1/tasks/{task_id}` - Delete task

Query parameters for task listing:
- `status` - Filter by status (pending, in_progress, completed, cancelled)
- `skip` - Pagination offset
- `limit` - Pagination limit (default: 100)

### Events
- `POST /api/v1/events?user_id={user_id}` - Create a new event
- `GET /api/v1/events?user_id={user_id}` - List events for a user
- `GET /api/v1/events/{event_id}` - Get event details
- `PUT /api/v1/events/{event_id}` - Update event
- `DELETE /api/v1/events/{event_id}` - Delete event

Query parameters for event listing:
- `start_date` - Filter events after this date (ISO format)
- `end_date` - Filter events before this date (ISO format)
- `skip` - Pagination offset
- `limit` - Pagination limit (default: 100)

## Example API Usage

### Create a User
```bash
curl -X POST "http://localhost:8000/api/v1/users" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan",
    "email": "juan@example.com",
    "bio": "Productivity enthusiast"
  }'
```

### Create a Task
```bash
curl -X POST "http://localhost:8000/api/v1/tasks?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Finish project",
    "description": "Complete the AI feature",
    "priority": "high",
    "deadline": "2026-12-31T23:59:59",
    "status": "pending"
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

## Database Models

### User
- `id` (PK): Unique identifier
- `name`: User's full name
- `email`: Unique email address
- `bio`: Optional user biography
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp
- Relationships: tasks, events

### Task
- `id` (PK): Unique identifier
- `user_id` (FK): Associated user
- `title`: Task title
- `description`: Optional task description
- `status`: Current status (pending, in_progress, completed, cancelled)
- `priority`: Task priority (low, medium, high, urgent)
- `deadline`: Optional deadline date
- `is_recurring`: Boolean flag for recurring tasks
- `recurrence_pattern`: Pattern for recurrence (daily, weekly, monthly)
- `completed_at`: Completion timestamp if completed
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Event
- `id` (PK): Unique identifier
- `user_id` (FK): Associated user
- `title`: Event title
- `description`: Optional event description
- `event_type`: Event type (meeting, deadline, reminder, personal, work, social)
- `start_time`: Event start time
- `end_time`: Event end time
- `location`: Optional event location
- `is_all_day`: Boolean flag for all-day events
- `is_recurring`: Boolean flag for recurring events
- `recurrence_pattern`: Pattern for recurrence (daily, weekly, monthly)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

## Documentation

- **API Documentation**: Available at `http://localhost:8000/docs` (Swagger UI)
- **Alternative Docs**: Available at `http://localhost:8000/redoc` (ReDoc)

## Development

### Running Tests
Tests can be added using pytest:
```bash
pip install pytest pytest-asyncio httpx
pytest
```

### Database Migrations
For production, consider using Alembic:
```bash
pip install alembic
alembic init alembic
```

### Code Formatting
```bash
pip install black isort
black app/
isort app/
```

### Linting
```bash
pip install pylint flake8
pylint app/
flake8 app/
```

## Deployment

### Docker
Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t dona_pepa_api .
docker run -p 8000:8000 --env-file .env dona_pepa_api
```

### Production Settings
For production, update `main.py`:
```python
uvicorn.run(
    "app.main:app",
    host="0.0.0.0",
    port=8000,
    reload=False,  # Disable reload
    workers=4,     # Multiple workers
)
```

## Troubleshooting

### Database Connection Error
- Verify PostgreSQL is running
- Check credentials in `.env`
- Ensure database exists

### Port Already in Use
```bash
python main.py --port 8001
```

### Module Import Errors
Ensure you're in the virtual environment and all dependencies are installed:
```bash
pip install -r requirements.txt --force-reinstall
```

## Future Enhancements

- [ ] Authentication and authorization (JWT)
- [ ] Pagination improvements
- [ ] Advanced filtering and search
- [ ] Task dependencies
- [ ] Notifications system
- [ ] AI-powered task suggestions
- [ ] Calendar integration
- [ ] File attachments
- [ ] Task analytics
- [ ] Collaboration features

## Contributing

Follow these guidelines:
1. Create feature branches from `main`
2. Follow PEP 8 style guide
3. Add docstrings to all functions
4. Include unit tests for new features
5. Update documentation

## License

This project is part of the Agents League Hackathon 2026.

## Support

For issues or questions, please reach out to the development team.
