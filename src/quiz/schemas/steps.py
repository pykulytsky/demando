from typing import List

from pydantic import BaseModel

from questions.schemas.base import Timestamped
from quiz.schemas.options import Option


class StepBase(BaseModel):
    title: str


class StepCreate(StepBase):
    quiz: int


class Step(StepBase, Timestamped):
    pk: int
    done: bool
    options: List[Option]

    class Config:
        orm_mode = True
