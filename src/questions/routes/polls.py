from base.database import Base, engine
from questions.router import ItemRouter
from questions.schemas import polls as schemas

from .. import models

Base.metadata.create_all(bind=engine)


polls_router = ItemRouter(
    model=models.Poll,
    get_schema=schemas.Poll,
    create_schema=schemas.PollCreate,
    update_schema=schemas.PollUpdate,
    prefix="/polls",
    tags=["polls"],
)
