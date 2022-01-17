from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from auth.schemas import User
from .base import Timestamped


class Question(Timestamped):
    pk: int
    body: str
    author: User
    likes_count: int
    likes: Optional[List[User]]
    created: datetime

    class Config:
        orm_mode = True


class QuestionCreate(BaseModel):
    body: str
    event: int


class QuestionCreateTest(BaseModel):
    body: str
    event: int
    author: int


class AuthenticatedQuestionCreate(QuestionCreate):
    author: int


class QuestionPatch(BaseModel):
    body: Optional[str] = None
    likes_count: Optional[int] = None
    likes: Optional[List[User]] = None
