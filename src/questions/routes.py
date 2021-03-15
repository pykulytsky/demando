from typing import List
from fastapi import APIRouter, Depends
from base.database import SessionLocal, engine, Base
from questions.schemas import Event
from sqlalchemy.orm import Session


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
    dependencies=[Depends(get_db)]
)


@router.get('/events', response_model=List[Event])
def get_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = crud.get_events(db, skip, limit)
