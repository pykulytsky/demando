from typing import List
from fastapi import Depends, HTTPException
from auth.backend import authenticate
from auth.schemas import User
from base.database import engine, Base, get_db
from questions.schemas import events as schemas
from sqlalchemy.orm import Session
from .. import models

from base.router import BaseCrudRouter

from auth.models import User as _User


Base.metadata.create_all(bind=engine)


event_router = BaseCrudRouter(
    model=models.Event,
    get_schema=schemas.Event,
    create_schema=schemas.EventCreate,
    update_schema=schemas.EventUpdate,
    prefix='/events',
    tags=['events'],
)


@event_router.get('/user/{user_pk}', response_model=List[schemas.Event])
async def get_events_by_user(user_pk, db: Session = Depends(get_db)):
    event = models.Event.manager(db).filter(owner_pk=user_pk)
    return event


@event_router.get('/my/', response_model=List[schemas.Event])
async def get_my_events(
    db: Session = Depends(get_db),
    user: User = Depends(authenticate)
):
    event = models.Event.manager(db).filter(owner_pk=user.pk)
    return event


@event_router.post(
    '/',
    response_model=schemas.Event, status_code=201)
async def create_event(
    event: schemas.EventCreate,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate)
):

    _event = models.Event.manager(db).create(disable_check=False, **event.__dict__, owner=user)
    return _event
