"""FastAPI application factory"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import get_settings
from app.database import create_all_tables
from app.routes import health, users, tasks, events

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown"""
    # Startup: Create database tables
    create_all_tables()
    yield
    # Shutdown logic here if needed


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title=settings.api_title,
        description=settings.api_description,
        version=settings.api_version,
        lifespan=lifespan,
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(health.router)
    app.include_router(users.router)
    app.include_router(tasks.router)
    app.include_router(events.router)
    
    @app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "message": "Welcome to Doña Pepa API",
            "version": settings.api_version,
            "docs": "/docs"
        }
    
    return app


# Create the application instance
app = create_app()
