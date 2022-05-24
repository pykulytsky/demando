from pydantic import BaseModel


class QuizAnonUser(BaseModel):
    username: str

    class Config:
        orm_mode = True
