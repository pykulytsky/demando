from fastapi import Depends
from sqlalchemy.orm import Session
from base.database import engine, Base, get_db
from questions.router import ItemRouter

from .. import models
from auth.models import User
from questions.schemas import polls as schemas

from auth.backend import authenticate


Base.metadata.create_all(bind=engine)


polls_router = ItemRouter(
    model=models.Poll,
    get_schema=schemas.Poll,
    create_schema=schemas.PollCreate,
    update_schema=schemas.PollUpdate,
    prefix='/polls',
    tags=['polls'],
)


@polls_router.post(
    '/', response_model=polls_router.get_schema, status_code=201
)
def create_poll(
    schema: polls_router.create_schema,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate)
):
    return polls_router.model.manager(db).create(
        **schema.__dict__,
        owner=user
    )
