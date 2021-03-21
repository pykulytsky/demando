from pydantic import BaseModel
from auth.schemas import User


class Option(BaseModel):
    pk: int
    name: str


class OptionCreate(BaseModel):
    name: str
    poll: int


class Vote(BaseModel):
    pk: int
    option: Option
    owner: User


class VoteCreate(BaseModel):
    poll: int
    option: int


class Poll(BaseModel):
    pk: int
    name: str
    owner: User
    options: Option
    votes: Vote


class PollCreate(BaseModel):
    name: str


class AuthenticatedPollCreate(PollCreate):
    owner: User


class PollUpdate(PollCreate):
    pass
