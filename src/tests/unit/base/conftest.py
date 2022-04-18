import pytest

from auth.models import User
from core.manager import BaseManager


@pytest.fixture
def manager(db):
    return BaseManager(User, db)
