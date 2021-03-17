import pytest
from tests.test_database import engine
from questions.crud import create_event, create_qeustion

from questions.schemas import (
    AuthenticatedEventCreate, AuthenticatedQuestionCreate)


@pytest.fixture
def event(db, user):
    _event = AuthenticatedEventCreate(
        name='test event',
        owner=user.pk
    )
    event = create_event(db, _event)
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
    question = create_qeustion(db, _question)
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
