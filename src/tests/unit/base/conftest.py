import pytest

from auth.models import User
from base.manager import BaseManager


@pytest.fixture
def manager(db):
    return BaseManager(User, db)
