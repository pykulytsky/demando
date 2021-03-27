
from demando.base.database import engine, Base
from demando.base.router import CrudRouter

from .. import models
from ..schemas import polls as schemas


Base.metadata.create_all(bind=engine)


options_router = CrudRouter(
    model=models.Option,
    get_schema=schemas.Option,
    create_schema=schemas.OptionCreate,
    update_schema=schemas.OptionCreate,
    prefix='/options',
    tags=['options'],
)
