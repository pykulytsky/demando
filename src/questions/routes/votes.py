from fastapi import Depends
from sqlalchemy.orm import Session
from base.database import engine, Base, get_db
from base.router import CrudRouter

from .. import models
from auth.models import User
from questions.schemas import polls as schemas

from auth.backend import authenticate


Base.metadata.create_all(bind=engine)


votes_router = CrudRouter(
    model=models.Vote,
    get_schema=schemas.Vote,
    create_schema=schemas.VoteCreate,
    update_schema=schemas.VoteCreate,
    prefix='/votes',
    tags=['votes'],
)


@votes_router.post(
    '/', response_model=votes_router.get_schema, status_code=201
)
def create_poll(
    schema: votes_router.create_schema,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate)
):
    return votes_router.model.manager(db).create(
        poll=models.Poll.manager(db).get(pk=schema.poll),
        option=models.Option.manager(db).get(pk=schema.option),
    )
