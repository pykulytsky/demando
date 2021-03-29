import pytest
from demando.auth.models import User
from demando.main import get_app
from fastapi.testclient import TestClient
from .test_client import JWTAuthTestClient

from tests.test_database import TestSessionLocal, engine
from demando.auth.schemas import UserCreate

from sqlalchemy.engine import reflection

from alembic.config import main
from demando.base.database import db
from starlette.config import environ


@pytest.fixture(scope="session")
def client():
    main(["--raiseerr", "upgrade", "head"])

    with TestClient(get_app()) as client:
        yield client

    main(["--raiseerr", "downgrade", "base"])


@pytest.fixture()
def auth_client(user):
    main(["--raiseerr", "upgrade", "head"])

    with JWTAuthTestClient(get_app(), user) as client:
        yield client

    main(["--raiseerr", "downgrade", "base"])


@pytest.fixture
async def user():
    _user = UserCreate(
        email='test1@test.py',
        username='test1',
        password='1234'
    )
    user = await User.manager().create_user(_user)
    yield user


@pytest.fixture
async def another_user():
    _user = UserCreate(
        email='test2@test.py',
        username='test2',
        password='1234'
    )
    user = await User.manager().create_user(_user)
    yield user
