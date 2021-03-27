from demando.auth.models import User
from demando.base.manager import BaseManager

import pytest


@pytest.fixture
def manager(db):
    return BaseManager(User, db)
