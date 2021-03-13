import pytest

from main import app, get_db
from fastapi.testclient import TestClient
from mixer.backend.sqlalchemy import mixer as _mixer
from base.database import Base

from tests.test_database import TestSessionLocal, engine

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mixer():
    return _mixer


def user(mixer):
    return mixer.blend('auth.models.User')
