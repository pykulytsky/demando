import pytest

from quiz.models import Quiz


@pytest.fixture
def quiz(db, user):
    return Quiz.manager(db).create(name="test quiz", owner=user)
