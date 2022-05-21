from typing import Optional

from pydantic import BaseModel

from questions.schemas.base import Timestamped


class OptionBase(BaseModel):
    title: str
    is_right: bool


class OptionCreate(OptionBase):
    step: int


class OptionPatch(BaseModel):
    title: Optional[str]
    is_right: Optional[bool]


class Option(OptionBase, Timestamped):
    pk: int

    class Config:
        orm_mode = True


class OptionWebsocket(OptionBase):
    pk: int

    class Config:
        orm_mode = True
