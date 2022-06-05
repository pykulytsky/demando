from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from auth.backend import authenticate
from auth.schemas import User
from core.database import Base, engine, get_db
from core.exceptions import ObjectDoesNotExists
from questions.router import ItemRouter
from questions.schemas import questions as schemas

from .. import models

Base.metadata.create_all(bind=engine)


questions_router = ItemRouter(
    model=models.Question,
    get_schema=schemas.Question,
    create_schema=schemas.QuestionCreate,
    update_schema=schemas.QuestionPatch,
    prefix="/questions",
    tags=["questions"],
)


@questions_router.get("/my/", response_model=List[schemas.Question])
async def get_my_questions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate),
):
    questions = models.Question.manager(db).filter(author_pk=user.pk)
    return questions


@questions_router.get("/event/{pk}", response_model=List[schemas.Question])
async def get_questions_by_event(pk: int, db: Session = Depends(get_db)):
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


@questions_router.patch("/{pk}/like/", response_model=schemas.Question)
async def like_question(
    pk: int, db: Session = Depends(get_db), user: User = Depends(authenticate)
):
    try:
        question = models.Question.manager(db).get(pk=pk)
    except ObjectDoesNotExists:
        raise HTTPException(404, detail=f"No question with pk={pk} was found.")
    for like in question.likes:
        if user == like:
            raise HTTPException(400, detail="User already liked question")

    question.likes.append(user)
    question.likes_count += 1
    db.commit()
    db.refresh(question)

    return question
