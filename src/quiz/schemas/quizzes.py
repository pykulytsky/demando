from typing import List, Optional

from pydantic import BaseModel

from auth.schemas import User
from questions.schemas.base import Timestamped
from quiz.schemas.steps import Step


class QuizBase(BaseModel):
    name: str


class QuizCreate(QuizBase):
    enter_code: Optional[str]
    seconds_per_answer: Optional[int]
    is_private: Optional[bool]
    delete_after_finish: Optional[bool]


class QuizPatch(BaseModel):
    name: Optional[str]
    enter_code: Optional[str]
    seconds_per_answer: Optional[int]
    is_private: Optional[bool]
    delete_after_finish: Optional[bool]


class Quiz(QuizBase, Timestamped):
    pk: int
    owner: User
    enter_code: str
    done: bool
    seconds_per_answer: int
    is_private: Optional[bool]
    delete_after_finish: Optional[bool]
    members: Optional[List[User]]
    steps: Optional[List[Step]]

    class Config:
        orm_mode = True
