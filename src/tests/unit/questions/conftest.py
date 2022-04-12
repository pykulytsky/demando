import pytest

from questions.models import Event, Option, Poll, Question
from questions.schemas.events import AuthenticatedEventCreate
from questions.schemas.questions import AuthenticatedQuestionCreate
from tests.test_database import engine


@pytest.fixture
def event(db, user):
    event = Event.manager(db).create(owner=user, name="test event")
    yield event

    cursor = engine.connect()
    cursor.execute("DELETE FROM questions;")
    cursor.execute("DELETE FROM events;")
    cursor.execute("DELETE FROM users;")


@pytest.fixture
def event_schema(user):
    _event = AuthenticatedEventCreate(name="test event 1", owner=user.pk)

    return _event


@pytest.fixture
def question(event, user, db):
    question = Question.manager(db).create(
        disable_check=False, body="test question", author=user, event=event
    )
    yield question

    cursor = engine.connect()
    cursor.execute("DELETE FROM questions;")
    cursor.execute("DELETE FROM events;")
    cursor.execute("DELETE FROM users;")


@pytest.fixture
def question_schema(user, event):
    _question = AuthenticatedQuestionCreate(
        body="test question", author=user.pk, event=event.pk
    )

    return _question


@pytest.fixture
def poll(user, db):
    poll = Poll.manager(db).create(name="klara or karl?", owner=user)

    return poll


@pytest.fixture
def option(db, poll):
    option = Option.manager(db).create(name="test question?", poll=poll)
    Option.manager(db).create(name="test question1?", poll=poll)
    Option.manager(db).create(name="test question2?", poll=poll)
    return option
