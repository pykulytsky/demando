from demando.auth.manager import AuthManager
from demando.auth.schemas import UserCreate
from demando.auth.models import User

import pytest


@pytest.fixture
def manager(db):
    return AuthManager(User, db)


@pytest.fixture
def user_schema():
    return UserCreate(username='stepan', email='bandera@ss.com', password='1488')
