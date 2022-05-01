from pydantic import BaseModel

from questions.schemas.base import Timestamped


class OptionBase(BaseModel):
    title: str
    is_right: bool


class OptionCreate(OptionBase):
    step: int


class Option(OptionBase, Timestamped):
    pk: int
    step: int

    class Config:
        orm_mode = True
