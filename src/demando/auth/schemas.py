from pydantic import BaseModel, EmailStr
from typing import Optional


class Role(BaseModel):
    pk: int
    verbose: str


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserAuth(BaseModel):
    email: EmailStr


class UserLogin(UserAuth):
    password: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    pk: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class Token(BaseModel):
    token: str
