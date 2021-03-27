import pytest
from demando.auth.models import User
from demando.main import app, get_db
from fastapi.testclient import TestClient
from .test_client import JWTAuthTestClient

from mixer.backend.sqlalchemy import Mixer

from demando.base.database import Base
from tests.test_database import TestSessionLocal, engine

from demando.auth.crud import create_user
from demando.auth.schemas import UserCreate

from sqlalchemy.engine import reflection


@pytest.fixture(autouse=True)
def create_models():
    Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestSessionLocal()
        yield db
    finally:
        db.close()


_mixer = Mixer(session=TestSessionLocal(), commit=True)


app.dependency_overrides[get_db] = override_get_db


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
        insp = reflection.Inspector.from_engine(engine)
        total_tables = insp.get_table_names()[::-1]

        con = engine.connect()
        for table in total_tables:
            if table != 'alembic_version':
                con.execute(f'DELETE FROM {table} CASCADE;')
        db.close()


@pytest.fixture
def user(db):
    _user = UserCreate(
        email='test1@test.py',
        username='test1',
        password='1234'
    )
    user = User.manager(db).create_user(_user)
    yield user


@pytest.fixture
def another_user(db):
    _user = UserCreate(
        email='test2@test.py',
        username='test2',
        password='1234'
    )
    user = User.manager(db).create_user(_user)
    yield user


@pytest.fixture
def auth_client(db, user):
    return JWTAuthTestClient(app, user=user, db=db)
