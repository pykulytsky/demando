from typing import List

from pydantic import BaseModel

from auth.schemas import User
from questions.schemas.base import Timestamped
from quiz.schemas.steps import Step


class QuizBase(BaseModel):
    name: str


class QuizCreate(QuizBase):
    owner: int


class Quiz(QuizBase, Timestamped):
    pk: int
    owner: User
    members: List[User]
    enter_code: str
    steps: List[Step]
