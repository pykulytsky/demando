from base.database import SessionLocal, engine, Base
from base.router import BaseCrudRouter

from .. import models
from questions.schemas import polls as schemas


Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


polls_router = BaseCrudRouter(
    model=models.Poll,
    get_schema=schemas.Poll,
    create_schema=schemas.PollCreate,
    update_schema=schemas.PollUpdate,
    prefix='/polls',
    tags=['polls'],
)
