from typing import Union
from sqlalchemy.orm import Session

from . import models, schemas
from auth.crud import get_user


def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()


def get_event(db: Session, int: id):
    return db.query(models.Event).filter(models.Event.id == id).first()


def create_event(db: Session, event: schemas.EventCreate):
    _event = models.Event(
        name=event.name,
        owner=get_user(db, event.owner.id)
    )

    db.add(_event)
    db.commit()
    db.refresh(_event)
    return _event


def get_question(db: Session, int: id):
    return db.query(models.Question).filter(models.Question.id == id).first()


def get_events_questions(db: Session, event_id):
    return db.query(models.Question).filter(
        models.Question.event_id == event_id
    ).all()


def get_questions_by_author(db: Session, author_id):
    return db.query(models.Question).filter(
        models.Question.author_id == author_id
    )


def create_qeustion(db: Session, question: schemas.QuestionCreate):
    _question = models.Question(
        body=question.body,
        author=get_user(db, question.author.id),
        event=get_event(db, question.event.id)
    )

    db.add(_question)
    db.commit()
    db.refresh(_question)
    return _question
