from core.database import Base, engine
from questions.router import ItemRouter
from quiz.models import Step
from quiz.schemas import steps

Base.metadata.create_all(bind=engine)


steps_router = ItemRouter(
    model=Step,
    get_schema=steps.Step,
    create_schema=steps.StepCreate,
    update_schema=steps.StepPatch,
    prefix="/steps",
    tags=["steps"],
)
