from fastapi import APIRouter

from core.database import Base, engine

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
