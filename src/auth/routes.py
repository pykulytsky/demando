from fastapi import APIRouter, Depends, HTTPException
from auth import crud, schemas
from typing import List
from sqlalchemy.orm import Session
from base.database import SessionLocal, engine, Base

from .backend import JWTAuthentication

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


@router.post("/users/", response_model=schemas.Token)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = crud.create_user(db=db, user=user)
    return {"token": new_user.token}


@router.post("/refresh/", response_model=schemas.Token)
def refresh_token(user: schemas.UserLogin, db: Session = Depends(get_db)):
    pass


@router.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get(
    "/users/{user_id}",
    response_model=schemas.User,
    dependencies=[Depends(JWTAuthentication())]
)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
