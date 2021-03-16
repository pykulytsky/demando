from typing import List, Optional
from pydantic import BaseModel
from auth.schemas import User


class EventCreate(BaseModel):
    name: str


class AuthenticatedEventCreate(EventCreate):
    owner: int


class Question(BaseModel):
    pk: int
    body: str
    author: User
    likes_count: int
    likes: Optional[List[User]]

    class Config:
        orm_mode = True


class Event(BaseModel):
    pk: int
    name: str
    questions: Optional[List[Question]]
    owner: User

    class Config:
        orm_mode = True


class QuestionCreate(BaseModel):
    body: str
    event: int
    author: int
