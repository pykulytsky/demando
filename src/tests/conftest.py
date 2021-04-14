from typing import Generator
import pytest
from auth.models import User
from main import app, get_db
from fastapi.testclient import TestClient
from .test_client import JWTAuthTestClient

from mixer.backend.sqlalchemy import Mixer

from base.database import Base
from tests.test_database import TestSessionLocal, engine

from auth.schemas import UserCreate

from tortoise.contrib.test import finalizer, initializer


@pytest.fixture(autouse=True)
@pytest.mark.asyncio
async def init_db():
    await initializer(
        modules=['auth', 'questions'],
        db_url='sqlite://:memory:',
    )
    yield
    await finalizer()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def event_loop(client: TestClient) -> Generator:
    yield client.task.get_loop()


@pytest.fixture()
async def user():
    _user = UserCreate(
        email='test12@test.py',
        username='test12',
        password='12342'
    )
    user = await User.create(**_user.dict())
    yield user
    await user.delete()


@pytest.fixture()
async def another_user():
    _user = UserCreate(
        email='test23@test.py',
        username='test23',
        password='12344'
    )
    user = await User.create(**_user.dict())
    yield user
    await user.delete()


@pytest.fixture()
def auth_client(user):
    return JWTAuthTestClient(app, user=user)
