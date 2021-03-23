from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from auth.backend import authenticate
from auth.schemas import User
from base.database import engine, Base, get_db
from questions.router import ItemRouter

from .. import models
from questions.schemas import questions as schemas


Base.metadata.create_all(bind=engine)


questions_router = ItemRouter(
    model=models.Question,
    get_schema=schemas.Question,
    create_schema=schemas.QuestionCreate,
    update_schema=schemas.QuestionPatch,
    prefix='/questions',
    tags=['questions'],
)


@questions_router.get('/my/', response_model=List[schemas.Question])
async def get_my_questions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate)
):
    questions = models.Question.manager(db).filter(author_pk=user.pk)
    return questions


# @questions_router.post('/', response_model=schemas.Question)
# async def create_question(
#     question: schemas.QuestionCreate,
#     db: Session = Depends(get_db),
#     user: User = Depends(authenticate)
# ):

#     _question = models.Question.manager(db).create(
#         body=question.body,
#         event=models.Event.manager(db).get(pk=question.event),
#         author=user
#     )
#     return _question
