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


@questions_router.get('/event/{pk}', response_model=List[schemas.Question])
async def get_questions_by_event(
    pk: int,
    db: Session = Depends(get_db)
):
    return models.Question.manager(db).filter(event_pk=pk)


# @questions_router.patch('/event/{pk}', response_model=schemas.Question)
# async def patch_question(
#     pk: int,
#     update_schema: schemas.QuestionPatch,
#     db: Session = Depends(get_db),
#     user: User = Depends(authenticate)
# ):
#     if 'likes_count' in update_schema.dict():
#         _question = models.Question.manager(db).update(
#             pk=pk,
#             **update_schema
#         )
