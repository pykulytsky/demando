from demando.base.database import engine, Base
from demando.questions.router import ItemRouter

from .. import models
from ..schemas import polls as schemas


Base.metadata.create_all(bind=engine)


polls_router = ItemRouter(
    model=models.Poll,
    get_schema=schemas.Poll,
    create_schema=schemas.PollCreate,
    update_schema=schemas.PollUpdate,
    prefix='/polls',
    tags=['polls'],
)
