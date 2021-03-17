from typing import List
from fastapi import APIRouter, Depends, HTTPException
from auth.backend import authenticate
from auth.schemas import User
from base.database import engine, Base, get_db
from questions.schemas import AuthenticatedEventCreate, Event, EventCreate
from sqlalchemy.orm import Session

from questions import crud

Base.metadata.create_all(bind=engine)


event_router = APIRouter(
    prefix='/events',
    tags=['events'],
)


@event_router.get('/', response_model=List[Event])
def get_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = crud.get_events(db, skip, limit)
    return events


@event_router.get('/{event_pk}', response_model=Event)
def get_event(event_pk, db: Session = Depends(get_db)):
    event = crud.get_event(db, event_pk)
    if event:
        return event
    else:
        raise HTTPException(status_code=400, detail="No such event found")


@event_router.get('/user/{user_pk}', response_model=List[Event])
def get_events_by_user(user_pk, db: Session = Depends(get_db)):
    event = crud.get_events_by_user(db, user_pk)
    return event


@event_router.get('/my/', response_model=List[Event])
def get_my_events(
    db: Session = Depends(get_db),
    user: User = Depends(authenticate)
):
    event = crud.get_events_by_user(db, user.pk)
    return event


@event_router.post(
    '/',
    response_model=Event, status_code=201)
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate)
):
    event = AuthenticatedEventCreate(owner=user.pk, name=event.name)
    _event = crud.create_event(db, event)
    return _event
