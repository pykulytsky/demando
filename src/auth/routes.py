from auth.backend import authenticate
from auth.models import User, Role
from base import settings
from base.router import CrudRouter
from base.database import get_db

from base.integrations.sendgrid.client import SendgridApp

from . import schemas
from .exceptions import WrongLoginCredentials

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, BackgroundTasks

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
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    db_user = await User.get_or_none(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = await User.create(**user.dict())

    client = SendgridApp(db)

    background_tasks.add_task(client.send_verification_mail, new_user.id)

    return {"token": new_user.token}


@auth_router.post("/refresh/", response_model=schemas.Token, status_code=200)
async def refresh_token(
    user: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    try:
        db_user = await User.login(user)
    except WrongLoginCredentials as e:
        raise HTTPException(status_code=403, detail=str(e))

    return {"token": db_user.token}


@auth_router.get('/me/', response_model=schemas.User)
async def get_me(
    user: auth_router.get_schema = Depends(authenticate),
):
    return user
