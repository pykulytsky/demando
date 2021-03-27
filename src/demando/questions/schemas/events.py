from typing import List, Optional
from pydantic import BaseModel
from demando.auth.schemas import User

from .questions import Question


class EventCreate(BaseModel):
    name: str


class AuthenticatedEventCreate(EventCreate):
    owner: int


class Event(BaseModel):
    pk: int
    name: str
    questions: Optional[List[Question]]
    owner: User

    class Config:
        orm_mode = True


class EventUpdate(BaseModel):
    name: str
