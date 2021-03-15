import pytest
from main import app
from auth import routes as auth_routes
from questions import routes as questions_routes
from fastapi.testclient import TestClient
from .test_client import JWTAuthTestClient

from mixer.backend.sqlalchemy import Mixer

from base.database import Base
from tests.test_database import TestSessionLocal, engine

from auth.crud import create_user
from auth.schemas import UserCreate


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestSessionLocal()
        yield db
    finally:
        db.close()


_mixer = Mixer(session=TestSessionLocal(), commit=True)


app.dependency_overrides[auth_routes.get_db] = override_get_db
app.dependency_overrides[questions_routes.get_db] = override_get_db


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


@pytest.fixture
def user(db):
    _user = UserCreate(
        email='test1@test.py',
        username='test1',
        password='1234'
    )
    user = create_user(db, _user)
    yield user

    cursor = engine.connect()
    cursor.execute('DELETE FROM events;')
    cursor.execute('DELETE FROM questions;')
    cursor.execute('DELETE FROM users;')


@pytest.fixture
def another_user(db):
    _user = UserCreate(
        email='test2@test.py',
        username='test2',
        password='1234'
    )
    user = create_user(db, _user)
    yield user

    cursor = engine.connect()
    cursor.execute('DELETE FROM users;')


@pytest.fixture
def auth_client(db, user):
    return JWTAuthTestClient(app, user=user, db=db)
