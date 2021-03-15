from typing import List, Optional
from pydantic import BaseModel
from auth.schemas import User


class EventCreate(BaseModel):
    name: str
    owner: int


class Question(BaseModel):
    pk: int
    body: str
    author: User
    likes_count: int
    likes: Optional[List[User]]


class Event(BaseModel):
    pk: int
    name: str
    questions: Optional[List[Question]]
    owner: User


class QuestionCreate(BaseModel):
    body: str
    event: int
    author: int
