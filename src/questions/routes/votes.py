from core.database import Base, engine
from questions.router import ItemRouter
from questions.schemas import polls as schemas

from .. import models

Base.metadata.create_all(bind=engine)


votes_router = ItemRouter(
    model=models.Vote,
    get_schema=schemas.Vote,
    create_schema=schemas.VoteCreate,
    update_schema=schemas.VoteCreate,
    prefix="/votes",
    tags=["votes"],
)
