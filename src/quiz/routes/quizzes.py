from core.database import Base, engine
from questions.router import ItemRouter
from quiz.models import Quiz
from quiz.schemas import quizzes

Base.metadata.create_all(bind=engine)


quizzes_router = ItemRouter(
    model=Quiz,
    get_schema=quizzes.Quiz,
    create_schema=quizzes.QuizCreate,
    update_schema=quizzes.QuizPatch,
    prefix="/quizzes",
    tags=["quizzes"],
)
