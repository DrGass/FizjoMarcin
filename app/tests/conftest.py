import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database


from main import create_app
from modules.database import Base, get_db
from modules.auth.oauth2 import get_current_user

app = create_app()

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db_engine():
    if not database_exists(SQLALCHEMY_DATABASE_URL):
        create_database(engine.url)
    Base.metadata.create_all(bind=engine)
    yield engine
    drop_database(SQLALCHEMY_DATABASE_URL)


@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()
    connection.begin()
    db = SessionTesting(bind=connection)
    yield db
    db.rollback()
    connection.close()


def override_validate_token():
    return {"email": "test.email@test.com"}


@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_current_user] = override_validate_token
    with TestClient(app) as c:
        yield c
