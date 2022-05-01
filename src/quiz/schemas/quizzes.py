from typing import List, Optional

from pydantic import BaseModel

from auth.schemas import User
from questions.schemas.base import Timestamped
from quiz.schemas.steps import Step


class QuizBase(BaseModel):
    name: str


class QuizCreate(QuizBase):
    enter_code: Optional[str]


class Quiz(QuizBase, Timestamped):
    pk: int
    owner: User
    members: Optional[List[User]]
    enter_code: str
    steps: Optional[List[Step]]
    done: bool

    class Config:
        orm_mode = True
