from fastapi import APIRouter, Depends, HTTPException
from auth import schemas
from typing import List
from sqlalchemy.orm import Session
from auth.models import User
from base.database import engine, Base, get_db

from .backend import JWTAuthentication, authenticate

Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post("/users/", response_model=schemas.Token, status_code=201)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    manager = User.manager(db)
    db_user = manager.exists(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = manager.create_user(user)
    return {"token": new_user.token}


@router.post("/refresh/", response_model=schemas.Token)
async def refresh_token(user: schemas.UserLogin, db: Session = Depends(get_db)):
    manager = User.manager(db)
    db_user = manager.login(user)

    return {"token": db_user.token}


@router.get("/users/", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = User.manager(db).all(skip=skip, limit=limit)
    return users


@router.get(
    "/users/{user_id}",
    response_model=schemas.User,
    dependencies=[Depends(JWTAuthentication())]
)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    manager = User.manager(db)
    db_user = manager.get(pk=user_id)

    return db_user


@router.get('/users/me/', response_model=schemas.User)
async def get_me(
    user: schemas.User = Depends(authenticate),
):
    return user
