from pydantic import BaseModel
from auth.schemas import User


class Poll(BaseModel):
    pk: int
    name: str
    owner: User


class PollCreate(BaseModel):
    name: str


class AuthenticatedPollCreate(PollCreate):
    owner: User


class PollUpdate(PollCreate):
    pass
