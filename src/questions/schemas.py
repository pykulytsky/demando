from typing import List, Optional
from pydantic import BaseModel
from auth.schemas import User


class EventCreate(BaseModel):
    name: str
    owner: User


class Question(BaseModel):
    pk: int
    body: str
    author: User
    likes_count: int
    likes: Optional[List[User]]


class Event(EventCreate):
    pk: int
    questions: Optional[List[Question]]


class QuestionCreate(BaseModel):
    body: str
    event: Event
    author: User
