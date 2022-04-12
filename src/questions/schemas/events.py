from typing import List, Optional

from pydantic import BaseModel

from auth.schemas import User

from .base import Timestamped
from .questions import Question


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
    name: Optional[str] = None
