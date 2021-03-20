from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.backend import authenticate
from auth.schemas import User
from base.database import engine, Base, get_db
from questions import schemas

from questions import crud


Base.metadata.create_all(bind=engine)


questions_router = APIRouter(
    prefix='/questions',
    tags=['questions'],
)


@questions_router.get('/{question_pk}', response_model=schemas.Question)
async def get_question(question_pk: int, db: Session = Depends(get_db)):
    question = crud.get_question(db, question_pk)
    return question


@questions_router.get('/my/', response_model=List[schemas.Question])
async def get_my_questions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate)
):
    questions = crud.get_questions_by_author(db, user.pk)
    return questions


@questions_router.get('/', response_model=List[schemas.Question])
async def get_questions_list(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    questions = crud.get_questions(db, skip, limit)
    return questions


@questions_router.patch('/{question_pk}', response_model=schemas.Question)
async def patch_question(
    question_pk: int,
    question: schemas.QuestionPatch,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate)
):
    new_question = crud.update_question(db, question_pk, question=question)
    return new_question


@questions_router.post('/', response_model=schemas.Question)
async def create_question(
    question: schemas.QuestionCreate,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate)
):
    question_auth_create_schema = schemas.AuthenticatedQuestionCreate(
        body=question.body,
        event=question.event,
        author=user.pk
    )

    _question = crud.create_qeustion(db, question_auth_create_schema)
    return _question
