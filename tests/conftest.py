import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from db import Base, get_db

########################################################################################################################
# Set up in-memory SQLite engine
# Using StaticPool to persist the database for all connections during tests
########################################################################################################################
SQLALCHEMY_TEST_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool  # keeps the DB alive across connections
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    """
    Provide a database session connected to the test database.

    Yields a SQLAlchemy session and ensures it is closed after use.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    """
    Pytest fixture to provide a TestClient connected to the FastAPI app.

    Yields:
        TestClient: A client that can be used to call API endpoints in tests.
    """
    with TestClient(app) as c:
        yield c