from pydantic import BaseModel, EmailStr, ValidationError, root_validator
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserLogin(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: str

    @root_validator(pre=True)
    def validate_login_credentials(cls, values):
        v = values.copy()
        v.pop('password')
        if len(v) > 1:
            raise ValidationError(
                "Only one of the following fields is allowed: email, username"
            )
        if len(v) < 1:
            raise ValidationError(
                "At least one of the following fields must be passed: email, username" # noqa
            )

        return values


class UserCreate(UserBase):
    password: str


class User(UserBase):
    pk: int
    role: Optional[int]
    email_verified: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    token: str
