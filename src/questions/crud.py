from sqlalchemy.orm import Session

from . import models
from .schemas import events
from .schemas import questions
from auth.crud import get_user


def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()


def get_event(db: Session, pk: int):
    return db.query(models.Event).filter(models.Event.pk == pk).first()


def create_event(db: Session, event: events.EventCreate):
    _event = models.Event(
        name=event.name,
        owner=get_user(db, event.owner)
    )

    db.add(_event)
    db.commit()
    db.refresh(_event)
    return _event


def get_events_by_user(db: Session, user_pk):
    return db.query(models.Event).filter(
        models.Event.owner_pk == user_pk
    ).all()


def get_question(db: Session, pk: int):
    return db.query(models.Question).filter(models.Question.pk == pk).first()


def get_events_questions(db: Session, event_pk):
    return db.query(models.Question).filter(
        models.Question.event_pk == event_pk
    ).all()


def get_questions_by_author(db: Session, author_pk):
    return db.query(models.Question).filter(
        models.Question.author_pk == author_pk
    ).all()


def create_qeustion(
    db: Session, question: questions.AuthenticatedQuestionCreate
):
    _question = models.Question(
        body=question.body,
        author=get_user(db, question.author),
        event=get_event(db, question.event)
    )

    db.add(_question)
    db.commit()
    db.refresh(_question)
    return _question


def get_questions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Question).offset(skip).limit(limit).all()


def update_question(
    db: Session, question_pk: int, patched_data: questions.QuestionPatch
):
    question = db.query(models.Question).filter(
        models.Question.pk == question_pk
    )

    if question:
        question.update({
            k: patched_data.__dict__[k]
            for k in patched_data.__dict__.keys()
            if patched_data.__dict__[k] is not None}
        )
        db.commit()
        db.refresh(question.first())

        return question.first()


def delete_question(db: Session, question_pk: int):
    question = db.query(models.Question).filter(
        models.Question.pk == question_pk
    ).first()

    db.delete(question)
    db.refresh(question)
    return 


def delete_event(db: Session, event_pk: int):
    event = db.query(models.Event).filter(
        models.Event.pk == event_pk
    ).first()

    db.delete(event)
    db.refresh(event)
    return event
