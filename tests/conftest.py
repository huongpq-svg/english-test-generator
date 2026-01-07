import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# Ensure src is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from database import Base, get_db
from api import app
from models import Question # Ensure this is imported so Base knows about it

# Use file-based SQLite for tests to avoid in-memory persistence issues
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db_session():
    # Create tables
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    
    # Verify tables
    from sqlalchemy import inspect
    inspector = inspect(engine)
    print(f"Tables in test DB: {inspector.get_table_names()}")
    
    session = TestingSessionLocal()
    
    # Mock Data
    print("Seeding test data...")
    q1 = Question(grade=5, category="Intermediate", type="Multiple Choice", subtype="vocab", 
                  question_text="Q1 Text", answer="A1", options=["A1", "B", "C", "D"])
    q2 = Question(grade=5, category="Intermediate", type="Essay", subtype="essay",
                  question_text="Write an essay", answer=None, options=None)
    session.add(q1)
    session.add(q2)
    session.commit()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
