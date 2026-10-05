"""Tell Us Once - FastAPI Application Entry Point."""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.models.database import create_tables, engine, SessionLocal
from app.data.seed_data import seed_departments

# Import all models so they are registered with Base
from app.models.case import Case  # noqa: F401
from app.models.request import Request  # noqa: F401
from app.models.department import Department  # noqa: F401
from app.models.audit import Timeline, AuditLog  # noqa: F401

# Import routers
from app.api.health import router as health_router
from app.api.departments import router as departments_router
from app.api.cases import router as cases_router
from app.api.intake import router as intake_router
from app.api.requests import router as requests_router
from app.api.demo import router as demo_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database and seed departments on startup."""
    logger.info("Starting Tell Us Once backend...")
    create_tables()

    # Seed departments if not already present
    db = SessionLocal()
    try:
        seed_departments(db)
        logger.info("Departments seeded successfully.")
    except Exception as e:
        logger.error(f"Error seeding departments: {e}")
    finally:
        db.close()

    logger.info("Tell Us Once backend started successfully.")
    logger.info(f"OpenAI API Key configured: {'Yes' if settings.OPENAI_API_KEY else 'No (using fallback)'}")
    
    yield
    
    """Cleanup on shutdown."""
    logger.info("Shutting down Tell Us Once backend...")

# Create FastAPI app
app = FastAPI(
    title="Tell Us Once",
    description="Student Welfare / Joined-Up Case Management MVP API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router, prefix="/api", tags=["Health"])
app.include_router(departments_router, prefix="/api", tags=["Departments"])
app.include_router(cases_router, prefix="/api", tags=["Cases"])
app.include_router(intake_router, prefix="/api", tags=["Intake"])
app.include_router(requests_router, prefix="/api", tags=["Requests"])
app.include_router(demo_router, prefix="/api", tags=["Demo"])
