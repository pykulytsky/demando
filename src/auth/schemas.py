from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    username: str


class UserAuth(BaseModel):
    email: str


class UserLogin(UserAuth):
    password: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    role: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    token: str
