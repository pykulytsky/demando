import pytest
from tests.test_database import engine
from questions.crud import create_event, create_qeustion

from questions.schemas import EventCreate, QuestionCreate, Event
from auth.schemas import User


@pytest.fixture
def event(db, user):
    _event = EventCreate(
        name='test event',
        owner=User(
            id=user.id,
            email=user.email,
            username=user.username
        )
    )
    event = create_event(db, _event)
    yield event

    cursor = engine.connect()
    cursor.execute('DELETE FROM events;')
    cursor.execute('DELETE FROM questions;')
    cursor.execute('DELETE FROM users;')


@pytest.fixture
def event_schema(user):
    _event = EventCreate(
        name='test event 1',
        owner=User(
            id=user.id,
            email=user.email,
            username=user.username
        )
    )

    return _event


@pytest.fixture
def question(event, user, db):
    _question = QuestionCreate(
        body='test question',
        author=User(
            id=user.id,
            email=user.email,
            username=user.username
        ),
        event=Event(
            id=event.id,
            name=event.name,
            owner=User(
                id=user.id,
                email=user.email,
                username=user.username
            ),
        )
    )
    question = create_qeustion(db, _question)
    yield question

    cursor = engine.connect()
    cursor.execute('DELETE FROM events;')
    cursor.execute('DELETE FROM questions;')
    cursor.execute('DELETE FROM users;')
