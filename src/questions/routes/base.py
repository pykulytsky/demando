from fastapi import APIRouter
from base.database import SessionLocal, engine, Base

from .events import event_router
from .pools import pools_router
from .questions import questions_router


Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    prefix='/qa',
    tags=['qa'],
)

router.include_router(event_router)
router.include_router(questions_router)
router.include_router(pools_router)
