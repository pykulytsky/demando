from pydantic import BaseModel
from auth.schemas import User
from typing import List, Optional
from .base import Timestamped


class BaseOption(Timestamped):
    pk: int
    name: str


class OptionCreate(BaseModel):
    name: str
    poll: int


class BaseVote(Timestamped):
    pk: int
    option: BaseOption

    class Config:
        orm_mode = True


class BasePoll(Timestamped):
    pk: int
    name: str


class Option(BaseOption):
    pk: int
    name: str
    votes: Optional[List[BaseVote]]

    class Config:
        orm_mode = True


class Vote(BaseVote):
    pk: int
    owner: User

    class Config:
        orm_mode = True


class VoteCreate(BaseModel):
    pk: int
    poll: int
    option: int


class Poll(BaseModel):
    pk: int
    name: str
    owner: User
    options: Optional[List[BaseOption]]
    votes: Optional[List[BaseVote]]

    class Config:
        orm_mode = True


class PollCreate(BaseModel):
    name: str


class AuthenticatedPollCreate(PollCreate):
    owner: User


class PollUpdate(PollCreate):
    pass
