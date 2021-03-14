from fastapi import APIRouter, Depends
from base.database import SessionLocal, engine, Base


Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    prefix='/auth',
    tags=['auth'],
    dependencies=[Depends(get_db)]
)
