
from fastapi import Depends
from sqlalchemy.orm import Session
from base.database import engine, Base, get_db
from base.router import CrudRouter

from .. import models
from auth.models import User
from questions.schemas import polls as schemas

from auth.backend import authenticate


Base.metadata.create_all(bind=engine)


options_router = CrudRouter(
    model=models.Option,
    get_schema=schemas.Option,
    create_schema=schemas.OptionCreate,
    update_schema=schemas.OptionCreate,
    prefix='/options',
    tags=['options'],
)


@options_router.post(
    '/', response_model=options_router.get_schema, status_code=201
)
def create_option(
    schema: options_router.create_schema,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate)
):
    return options_router.model.manager(db).create(
        name=schema.name,
        poll=models.Poll.manager(db).get(pk=schema.poll)
    )
