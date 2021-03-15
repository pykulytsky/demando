from questions import crud
import pytest


def test_get_events_empty(db):
    assert crud.get_events(db) == []


def test_get_events(db, event):
    assert crud.get_events(db)[0] == event


def test_create_event(db, event_schema):
    assert crud.create_event(db, event_schema) is not None


def test_get_questions_by_event_empty(db, event):
    assert crud.get_events_questions(db, event_id=event.id) == []


def test_get_questions_by_event(db, event, question):
    assert crud.get_events_questions(db, event_id=event.id)[0] == question
