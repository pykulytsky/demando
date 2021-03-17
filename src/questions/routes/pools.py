from fastapi import APIRouter
from base.database import SessionLocal, engine, Base


Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


pools_router = APIRouter(
    prefix='/pools',
    tags=['pools'],
)


