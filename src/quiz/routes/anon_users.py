from questions.router import ItemRouter
from quiz.models import QuizAnonUser
from quiz.schemas import anon_users


anon_users_router = ItemRouter(
    model=QuizAnonUser,
    get_schema=anon_users.QuizAnonUser,
    create_schema=anon_users.QuizAnonUser,
    update_schema=anon_users.QuizAnonUser,
    prefix="/anon_users",
    tags=["anon_users"],
)
