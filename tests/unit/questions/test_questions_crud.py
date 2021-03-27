from demando.questions import crud
from demando.questions.schemas import questions


def test_get_events_empty(db):
    assert crud.get_events(db) == []


def test_get_event(db, event):
    assert crud.get_event(db, event.pk) == event


def test_get_events(db, event):
    assert crud.get_events(db)[0] == event


def test_create_event(db, event_schema):
    assert crud.create_event(db, event_schema) is not None


def test_get_question(db, question):
    assert crud.get_question(db, question.pk) == question


def test_get_questions_by_event_empty(db, event):
    assert crud.get_events_questions(db, event_pk=event.pk) == []


def test_get_questions_by_event(db, event, question):
    assert crud.get_events_questions(db, event_pk=event.pk)[0] == question


def test_create_question(db, question_schema):
    assert crud.create_qeustion(db, question_schema)


def test_get_question_by_user(db, question, user):
    assert crud.get_questions_by_author(db, user.pk)[0] == question


def test_update_question(db, question):
    body = question.body

    updated_question = crud.update_question(
        db, question_pk=question.pk, patched_data=questions.QuestionPatch(
            body='changed!!!!'
        )
    )

    assert updated_question.body != body
