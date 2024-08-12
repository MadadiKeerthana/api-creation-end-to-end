from fastapi.testclient import TestClient
import pytest
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db, Base
# from alembic import command

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    #command.downgrade("base")
    #command.upgrade("head")
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    
    
@pytest.fixture
def client(session):
    #everything before yeild runs before the testcase
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestClient(app) 
    
    #everything after the yield runs after the testcase