from core.database import Base, engine
from questions.router import ItemRouter
from questions.schemas import polls as schemas

from .. import models

Base.metadata.create_all(bind=engine)


options_router = ItemRouter(
    model=models.Option,
    get_schema=schemas.Option,
    create_schema=schemas.OptionCreate,
    update_schema=schemas.OptionUpdate,
    prefix="/options",
    tags=["options"],
)
