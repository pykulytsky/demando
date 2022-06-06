from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, ValidationError, root_validator


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserLogin(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: str

    @root_validator(pre=True)
    def validate_login_credentials(cls, values):
        v = values.copy()
        v.pop("password")
        if len(v) > 1:
            raise ValidationError(
                "Only one of the following fields is allowed: email, username"
            )
        if len(v) < 1:
            raise ValidationError(
                "At least one of the following fields must be passed: email, username"  # noqa
            )

        return values


class UserCreate(UserBase):
    password: str


class EventNested(BaseModel):
    pk: int
    name: str

    class Config:
        orm_mode = True


class QuestionNested(BaseModel):
    pk: int
    body: str

    class Config:
        orm_mode = True


class PollNested(BaseModel):
    pk: int
    name: str
    multiply_votes: bool
    allowed_votes: int
    limited_time: bool
    time_to_vote: Optional[datetime]

    class Config:
        orm_mode = True


class VoteNested(BaseModel):
    pk: int

    class Config:
        orm_mode = True


class QuizNested(BaseModel):
    pk: int
    enter_code: str
    done: bool
    seconds_per_answer: int
    is_private: Optional[bool]
    delete_after_finish: Optional[bool]
    cover: Optional[str]

    class Config:
        orm_mode = True


class AnswerNested(BaseModel):
    pk: int
    time_to_estimate: int
    rank: int

    class Config:
        orm_mode = True


class User(UserBase):
    pk: int
    role: Optional[int]
    email_verified: bool
    first_name: Optional[str]
    last_name: Optional[str]
    age: Optional[int]
    country: Optional[str]

    class Config:
        orm_mode = True


class UserDetail(User):
    avatar: Optional[str]

    events: List[EventNested]
    questions: List[QuestionNested]
    polls: List[PollNested]
    quizzes: List[QuizNested]
    votes: List[VoteNested]
    answers: List[AnswerNested]

    class Config:
        orm_mode = True


class UserPatch(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    country: Optional[str] = None


class Token(BaseModel):
    token: str
