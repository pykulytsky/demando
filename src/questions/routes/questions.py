from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.backend import authenticate
from auth.schemas import User
from base.database import engine, Base, get_db
from questions.schemas import QuestionCreate, Question, AuthenticatedQuestionCreate

from questions import crud


Base.metadata.create_all(bind=engine)


questions_router = APIRouter(
    prefix='/questions',
    tags=['questions'],
)


@questions_router.get('/{question_pk}', response_model=Question)
def get_question(question_pk: int, db: Session = Depends(get_db)):
    question = crud.get_question(db, question_pk)
    return question


@questions_router.get('/my/', response_model=List[Question])
def get_my_questions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user: User = Depends(authenticate)):
    questions = crud.get_questions_by_author(db, user.pk)
    return questions


@questions_router.get('/', response_model=List[Question])
def get_questions_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    questions = crud.get_questions(db, skip, limit)
    return questions


@questions_router.patch('/', response_model=Question)
def patch_question()


@questions_router.post('/', response_model=Question)
def create_question(question: QuestionCreate, db: Session = Depends(get_db), user: User = Depends(authenticate)):
    question_auth_create_schema = AuthenticatedQuestionCreate(
        body=question.body,
        event=question.event,
        author=user.pk
    )

    _question = crud.create_qeustion(db, question_auth_create_schema)
    return _question
