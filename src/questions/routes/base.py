from fastapi import APIRouter
from base.database import engine, Base

from .pools import pools_router
from .questions import questions_router
from ..models import Event
from .. import schemas

from base.router import BaseCrudRouter


Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix='/qa',
    tags=['qa'],
)

event_router = BaseCrudRouter(
    model=Event,
    get_schema=schemas.Event,
    create_schema=schemas.EventCreate,
    update_schema=schemas.EventCreate,
    prefix='/events',
    tags=['events']
)

router.include_router(event_router)
router.include_router(questions_router)
router.include_router(pools_router)
