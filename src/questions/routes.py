from typing import List
from fastapi import APIRouter, Depends, HTTPException
from auth.backend import JWTAuthentication, decode_token
from auth.schemas import User
from base.database import SessionLocal, engine, Base
from questions.schemas import AuthenticatedEventCreate, Event, EventCreate
from sqlalchemy.orm import Session

from . import crud


Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    prefix='/qa',
    tags=['qa'],
    dependencies=[Depends(get_db)]
)


@router.get('/events/', response_model=List[Event])
def get_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = crud.get_events(db, skip, limit)
    return events


@router.get('/events/{event_pk}', response_model=Event)
def get_event(event_pk, db: Session = Depends(get_db)):
    event = crud.get_event(db, event_pk)
    if event:
        return event
    else:
        raise HTTPException(status_code=400, detail="No such event found")


@router.get('/{user_pk}/events/', response_model=Event)
def get_events_by_user(user_pk, db: Session = Depends(get_db)):
    event = crud.get_events_by_user(db, user_pk)
    return event


@router.post(
    '/events/',
    response_model=Event)
def create_event(event: EventCreate, db: Session = Depends(get_db), user: User = Depends(decode_token)):
    event = AuthenticatedEventCreate(owner=user.pk, name=event.name)
    _event = crud.create_event(db, event)
    return _event
