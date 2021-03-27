from demando.base.database import engine, Base
from ..router import ItemRouter

from .. import models
from ..schemas import polls as schemas


Base.metadata.create_all(bind=engine)


votes_router = ItemRouter(
    model=models.Vote,
    get_schema=schemas.Vote,
    create_schema=schemas.VoteCreate,
    update_schema=schemas.VoteCreate,
    prefix='/votes',
    tags=['votes'],
)
