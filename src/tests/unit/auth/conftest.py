import pytest

from auth.crud import create_user
from auth.schemas import UserCreate

from tests.test_database import engine


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
    cursor.execute('DELETE FROM users;')
