from pydantic import BaseModel
from auth.schemas import User
from typing import List, Optional


class BaseOption(BaseModel):
    pk: int
    name: str


class OptionCreate(BaseModel):
    name: str
    poll: int


class BaseVote(BaseModel):
    pk: int
    option: BaseOption


class BasePoll(BaseModel):
    pk: int
    name: str


class Option(BaseOption):
    votes: Optional[List[BaseVote]]
    poll: BasePoll


class Vote(BaseVote):
    owner: User

    class Config:
        orm_mode = True


class VoteCreate(BaseModel):
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
