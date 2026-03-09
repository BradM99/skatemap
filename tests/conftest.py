import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database.db_models import Spot
from main import app
from database.db import Base, get_db

SQLALCHEMY_TEST_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """
    Create all tables before each test and drop them afterwards
    to ensure complete isolation between tests.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    """
    Provide a database session connected to the test database.
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
    Provide a TestClient connected to the FastAPI app.
    """
    with TestClient(app) as c:
        yield c


@pytest.fixture
def db():
    """
    Provide a SQLAlchemy session connected to the test database.
    """
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def spot(db):
    spot = Spot(
        name="Test Spot",
        description="Fixture test spot",
        latitude=51.5074,
        longitude=-0.1278,
    )

    db.add(spot)
    db.commit()
    db.refresh(spot)

    return spot