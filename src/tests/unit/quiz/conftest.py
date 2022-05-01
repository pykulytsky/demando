import pytest

from quiz.models import Quiz, Step


@pytest.fixture
def quiz(db, user):
    return Quiz.manager(db).create(name="test quiz", owner=user)


@pytest.fixture
def step(db, quiz):
    return Step.manager(db).create(title="question 11", quiz=quiz)
