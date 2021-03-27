from typing import List, Optional
from pydantic import BaseModel
from demando.auth.schemas import User


class Question(BaseModel):
    pk: int
    body: str
    author: User
    likes_count: int
    likes: Optional[List[User]]

    class Config:
        orm_mode = True


class QuestionCreate(BaseModel):
    body: str
    event: int


class AuthenticatedQuestionCreate(QuestionCreate):
    author: int


class QuestionPatch(BaseModel):
    body: Optional[str]
    likes_count: Optional[int]
    likes: Optional[List[User]]

    class Config:
        orm_mode = True
