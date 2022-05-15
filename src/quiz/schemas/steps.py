from typing import List, Optional

from pydantic import BaseModel

from questions.schemas.base import Timestamped
from quiz.schemas.options import Option, OptionWebsocket


class StepBase(BaseModel):
    title: str


class StepCreate(StepBase):
    quiz: int


class StepPatch(BaseModel):
    title: Optional[str]
    done: Optional[bool]


class Step(StepBase, Timestamped):
    pk: int
    done: bool
    options: Optional[List[Option]]

    class Config:
        orm_mode = True


class StepWebsocket(StepBase):
    pk: int
    done: bool
    options: Optional[List[OptionWebsocket]]

    class Config:
        orm_mode = True
