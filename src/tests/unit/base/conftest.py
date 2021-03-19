from auth.models import User
from base.manager import BaseManager

import pytest


@pytest.fixture
def manager(db):
    return BaseManager(User, db)
