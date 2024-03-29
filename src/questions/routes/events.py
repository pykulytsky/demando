from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from auth.backend import authenticate
from auth.schemas import User
from core.database import Base, engine, get_db
from questions.router import ItemRouter
from questions.schemas import events as schemas

from .. import models

Base.metadata.create_all(bind=engine)


event_router = ItemRouter(
    model=models.Event,
    get_schema=schemas.Event,
    create_schema=schemas.EventCreate,
    update_schema=schemas.EventUpdate,
    prefix="/events",
    tags=["events"],
)


@event_router.get("/user/{user_pk}", response_model=List[schemas.Event])
async def get_events_by_user(user_pk, db: Session = Depends(get_db)):
    event = models.Event.manager(db).filter(owner_pk=user_pk)
    return event


@event_router.get("/my/", response_model=List[schemas.Event])
async def get_my_events(
    db: Session = Depends(get_db), user: User = Depends(authenticate)
):
    event = models.Event.manager(db).filter(owner_pk=user.pk)
    return event
