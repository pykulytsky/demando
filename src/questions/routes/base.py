from fastapi import APIRouter
from base.database import engine, Base

from .events import event_router
from .polls import polls_router
from .options import options_router
from .questions import questions_router
from .votes import votes_router


Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix='/qa',
    tags=['qa'],
)


router.include_router(event_router)
router.include_router(polls_router)
router.include_router(questions_router)
router.include_router(options_router)
router.include_router(votes_router)
