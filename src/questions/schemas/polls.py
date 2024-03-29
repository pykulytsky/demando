from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from auth.schemas import User

from .base import Timestamped


class BaseOption(BaseModel):
    pk: int
    name: str


class OptionCreate(BaseModel):
    name: str
    poll: int


class BaseVote(BaseModel):
    pk: int
    owner: Optional[User]
    owner_host: Optional[str]

    class Config:
        orm_mode = True


class BasePoll(Timestamped):
    pk: int
    name: str


class Option(BaseOption):
    name: str
    votes: Optional[List[BaseVote]]

    class Config:
        orm_mode = True


class OptionUpdate(BaseModel):
    name: Optional[str] = None


class Vote(BaseVote):
    owner: Optional[User]
    option: Option

    class Config:
        orm_mode = True


class VoteCreate(BaseModel):
    poll: int
    option: int


class Poll(BaseModel):
    pk: int
    name: str
    multiply_votes: bool
    allowed_votes: int
    limited_time: bool
    time_to_vote: Optional[datetime]
    login_required: bool
    owner: User
    options: Optional[List[Option]]
    votes: Optional[List[BaseVote]]

    class Config:
        orm_mode = True


class PollViaWeboscket(BaseModel):
    pk: int
    name: str
    multiply_votes: bool
    allowed_votes: int
    options: Optional[List[Option]]
    votes: Optional[List[BaseVote]]

    class Config:
        orm_mode = True


class PollCreate(BaseModel):
    name: str
    multiply_votes: Optional[bool]
    allowed_votes: Optional[int]
    limited_time: Optional[bool]
    time_to_vote: Optional[datetime]
    login_required: Optional[bool]


class AuthenticatedPollCreate(PollCreate):
    owner: User


class PollUpdate(BaseModel):
    name: Optional[str] = None
    multiply_votes: Optional[bool]
    allowed_votes: Optional[int]
    limited_time: Optional[bool]
    time_to_vote: Optional[datetime]
    login_required: Optional[bool]
