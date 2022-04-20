from random import randint

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from core.database import Base
from core.manager import BaseManagerModel
from quiz.manager import OptionManagerMixin
from core.models import Timestamped

member_table = Table(
    "quiz_members",
    Base.metadata,
    Column("user_pk", Integer, ForeignKey("users.pk"), nullable=True),
    Column("quiz_pk", Integer, ForeignKey("quizzes.pk"), nullable=True),
)


def _generate_enter_code() -> str:
    resulted_code = ""
    for _ in range(4):
        resulted_code += str(randint(1, 9))

    return resulted_code


class Quiz(Timestamped, BaseManagerModel):

    __tablename__ = "quizzes"

    pk = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=False)

    owner_pk = Column(Integer, ForeignKey("users.pk"))
    owner = relationship("User", back_populates="quizzes")

    members = relationship("User", secondary=member_table)

    enter_code = Column(String, unique=True, default=_generate_enter_code())

    steps = relationship("Step", back_populates="quiz")


class Step(Timestamped, BaseManagerModel):

    __tablename__ = "step"

    pk = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=False)
    done = Column(Boolean, default=False)

    quiz_pk = Column(Integer, ForeignKey("quizzes.pk"))
    quiz = relationship("Quiz", back_populates="steps")

    options = relationship("StepOption", back_populates="step")


class StepOption(Timestamped, OptionManagerMixin):

    __tablename__ = "step_option"

    pk = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    is_right = Column(Boolean)

    step_pk = Column(Integer, ForeignKey("step.pk"))
    step = relationship("Step", back_populates="options")
