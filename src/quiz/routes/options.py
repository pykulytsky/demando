from core.database import Base, engine
from questions.router import ItemRouter
from quiz.models import StepOption
from quiz.schemas import options

Base.metadata.create_all(bind=engine)


options_router = ItemRouter(
    model=StepOption,
    get_schema=options.Option,
    create_schema=options.OptionCreate,
    update_schema=options.OptionPatch,
    prefix="/options",
    tags=["options"],
)
