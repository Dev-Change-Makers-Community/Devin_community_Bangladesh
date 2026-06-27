"""Test configuration and fixtures."""

import pytest
import tempfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.database import get_db, Base
from app.auth import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from jose import jwt


# Test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create test engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def db():
    """Create test database tables."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(db):
    """Create a fresh database session for each test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    """Create test client with database override."""
    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session):
    """Create a test user."""
    from app.models import User
    from app.auth import get_password_hash
    
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpassword")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_user_token(test_user):
    """Create JWT token for test user."""
    access_token = jwt.encode(
        data={"sub": test_user.username}, 
        secret=SECRET_KEY, 
        algorithm=ALGORITHM
    )
    return access_token


@pytest.fixture
def auth_headers(test_user_token):
    """Create authorization headers for test requests."""
    return {"Authorization": f"Bearer {test_user_token}"}


@pytest.fixture
def test_expenses(db_session, test_user):
    """Create test expenses for the test user."""
    from app.models import Expense
    from datetime import datetime
    
    expenses = [
        Expense(
            title="Grocery Shopping",
            description="Weekly groceries",
            amount=150.50,
            category="Food",
            date=datetime(2024, 1, 15),
            owner_id=test_user.id
        ),
        Expense(
            title="Gas Station",
            description="Monthly gas",
            amount=60.00,
            category="Transport",
            date=datetime(2024, 1, 20),
            owner_id=test_user.id
        ),
        Expense(
            title="Netflix Subscription",
            description="Monthly subscription",
            amount=15.99,
            category="Entertainment",
            date=datetime(2024, 1, 25),
            owner_id=test_user.id
        )
    ]
    
    for expense in expenses:
        db_session.add(expense)
    
    db_session.commit()
    return expenses
