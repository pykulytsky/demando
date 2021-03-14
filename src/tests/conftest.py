import pytest
from main import app
from auth import routes as auth_routes
from fastapi.testclient import TestClient

from mixer.backend.sqlalchemy import Mixer

from base.database import Base
from tests.test_database import TestSessionLocal, engine


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestSessionLocal()
        yield db
    finally:
        db.close()


_mixer = Mixer(session=TestSessionLocal(), commit=True)


app.dependency_overrides[auth_routes.get_db] = override_get_db


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mixer():
    return _mixer


@pytest.fixture
def db():
    try:
        db = TestSessionLocal()
        yield db
    finally:
        db.close()
