"""Pytest configuration and test fixtures."""

import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Override database URL BEFORE importing app
os.environ["DATABASE_URL"] = "sqlite:///./test_tell_us_once.db"
os.environ["OPENAI_API_KEY"] = ""  # Ensure fallback is used in tests

from app.models.database import Base, get_db
from app.models.department import Department
from app.models.case import Case
from app.models.request import Request
from app.models.audit import Timeline, AuditLog
from app.main import app
from app.data.seed_data import seed_departments

# Test database
TEST_DATABASE_URL = "sqlite:///./test_tell_us_once.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    """Override the database dependency for tests."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    """Create tables before each test and drop after."""
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    seed_departments(db)
    db.close()
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def db():
    """Create a test database session."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
