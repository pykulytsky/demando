from fastapi import APIRouter

from core.database import Base, engine

from .anon_users import anon_users_router
from .options import options_router
from .quizzes import quizzes_router
from .steps import steps_router

Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/quiz",
    tags=["quiz"],
)


router.include_router(quizzes_router)
router.include_router(steps_router)
router.include_router(options_router)
router.include_router(anon_users_router)
