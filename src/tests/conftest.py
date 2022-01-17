import pytest
from auth.models import User
from main import app, get_db
from fastapi.testclient import TestClient
from .test_client import JWTAuthTestClient

from mixer.backend.sqlalchemy import Mixer

from base.database import Base
from tests.test_database import TestSessionLocal, engine

from auth.schemas import UserCreate

from sqlalchemy.engine import reflection


@pytest.fixture(autouse=True, scope="session")
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


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture(scope="session")
def mixer():
    return _mixer


@pytest.fixture()
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


@pytest.fixture()
def user(db):
    _user = UserCreate(
        email='test1@test.py',
        username='test1',
        password='1234',
    )
    user = User.manager(db).create_user(_user)
    user.email_verified = True
    db.commit()
    db.refresh(user)
    yield user


@pytest.fixture()
def another_user(db):
    _user = UserCreate(
        email='test2@test.py',
        username='test2',
        password='1234'
    )
    user = User.manager(db).create_user(_user)
    user.email_verified = True
    yield user


@pytest.fixture()
def unverified_user(db):
    _user = UserCreate(
        email='test3@test.py',
        username='test3',
        password='1234'
    )
    user = User.manager(db).create_user(_user)
    yield user


@pytest.fixture()
def auth_client(db, user):
    return JWTAuthTestClient(app, user=user, db=db)


@pytest.fixture()
def unverified_auth_client(db, unverified_user):
    return JWTAuthTestClient(app, user=unverified_user, db=db)
