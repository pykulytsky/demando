from typing import List, Optional
from pydantic import BaseModel
from auth.schemas import User


class EventCreate(BaseModel):
    name: str
    owner: User


class Event(EventCreate):
    id: int
    questions: Optional[List['Question']]


class QuestionCreate(BaseModel):
    body: str
    event: Event
    author: User


class Question(QuestionCreate):
    id: int
    likes_count: int
    likes: Optional[List[User]]
