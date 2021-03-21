import pytest
from tests.test_database import engine

from questions.models import Event, Question
from auth.models import User

from questions.schemas.questions import AuthenticatedQuestionCreate
from questions.schemas.events import AuthenticatedEventCreate


@pytest.fixture
def event(db, user):
    _event = AuthenticatedEventCreate(
        name='test event',
        owner=user.pk
    )
    event = Event.manager(db).create(owner=user, name='test event')
    yield event

    cursor = engine.connect()
    cursor.execute('DELETE FROM questions;')
    cursor.execute('DELETE FROM events;')
    cursor.execute('DELETE FROM users;')


@pytest.fixture
def event_schema(user):
    _event = AuthenticatedEventCreate(
        name='test event 1',
        owner=user.pk
    )

    return _event


@pytest.fixture
def question(event, user, db):
    _question = AuthenticatedQuestionCreate(
        body='test question',
        author=user.pk,
        event=event.pk
    )
    question = Question.manager(db).create(disable_check=False, body='test question', author=user, event=event)
    yield question

    cursor = engine.connect()
    cursor.execute('DELETE FROM questions;')
    cursor.execute('DELETE FROM events;')
    cursor.execute('DELETE FROM users;')


@pytest.fixture
def question_schema(user, event):
    _question = AuthenticatedQuestionCreate(
        body='test question',
        author=user.pk,
        event=event.pk
    )

    return _question
