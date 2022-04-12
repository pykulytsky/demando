import pytest

from auth.manager import AuthManager
from auth.models import User
from auth.schemas import UserCreate


@pytest.fixture
def manager(db):
    return AuthManager(User, db)


@pytest.fixture
def user_schema():
    return UserCreate(username="stepan", email="bandera@ss.com", password="1488")
