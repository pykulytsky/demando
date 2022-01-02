from typing import List, Optional
from pydantic import BaseModel
from auth.schemas import User

from .questions import Question
from .base import Timestamped


class EventCreate(BaseModel):
    name: str


class AuthenticatedEventCreate(EventCreate):
    owner: int


class Event(Timestamped):
    pk: int
    name: str
    questions: Optional[List[Question]]
    owner: User

    class Config:
        orm_mode = True


class EventUpdate(BaseModel):
    name: str
