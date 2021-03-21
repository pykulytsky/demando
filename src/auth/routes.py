from auth.backend import authenticate
from auth.models import User
from base.router import CrudRouter
from base.database import get_db

from . import schemas
from .exceptions import WrongLoginCredentials

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException


auth_router = CrudRouter(
    model=User,
    get_schema=schemas.User,
    create_schema=schemas.UserCreate,
    update_schema=schemas.UserBase,
    prefix='/auth/users',
    tags=['auth']
)


@auth_router.post('/', response_model=schemas.Token, status_code=201)
async def create_user(
    user: auth_router.create_schema,
    db: Session = Depends(get_db)
):
    manager = auth_router.model.manager(db)
    db_user = manager.exists(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = manager.create_user(user)
    return {"token": new_user.token}


@auth_router.post("/refresh/", response_model=schemas.Token)
async def refresh_token(
    user: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    manager = auth_router.model.manager(db)
    try:
        db_user = manager.login(user)
    except WrongLoginCredentials as e:
        raise HTTPException(status_code=403, detail=str(e))

    return {"token": db_user.token}


@auth_router.get('/me/', response_model=schemas.User)
async def get_me(
    user: auth_router.get_schema = Depends(authenticate),
):
    return user
