from random import randint

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from core.database import Base
from core.manager import BaseManagerMixin
from core.models import Timestamped
from quiz.manager import OptionManagerMixin, QuizManagerMixin

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


class Quiz(Timestamped, QuizManagerMixin):

    __tablename__ = "quizzes"

    pk = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=False)
    enter_code = Column(String, unique=True)
    seconds_per_answer = Column(Integer, default=30)
    is_private = Column(Boolean, default=False)
    delete_after_finish = Column(Boolean, default=False)
    cover = Column(String, nullable=True)

    owner_pk = Column(Integer, ForeignKey("users.pk"))
    owner = relationship("User", back_populates="quizzes")

    members = relationship("User", secondary=member_table)

    steps = relationship("Step", back_populates="quiz", order_by="Step.pk")

    @property
    def done(self):
        if self.steps:
            return all([step.done for step in self.steps])
        return False


class Step(Timestamped, BaseManagerMixin):

    __tablename__ = "steps"

    pk = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=False)
    done = Column(Boolean, default=False)

    quiz_pk = Column(Integer, ForeignKey("quizzes.pk"))
    quiz = relationship("Quiz", back_populates="steps")

    options = relationship("StepOption", back_populates="step")


class StepOption(Timestamped, OptionManagerMixin):

    __tablename__ = "step_options"

    pk = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=False)
    is_right = Column(Boolean)

    step_pk = Column(Integer, ForeignKey("steps.pk"))
    step = relationship("Step", back_populates="options")

    answers = relationship("Answer", back_populates="step_option")


class QuizAnonUser(Timestamped, BaseManagerMixin):

    __tablename__ = "quiz_anon_users"

    pk = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=False)

    answers = relationship("Answer", back_populates="anon_member")


class Answer(Timestamped, BaseManagerMixin):

    __tablename__ = "answers"

    pk = Column(Integer, primary_key=True, index=True)
    member_pk = Column(Integer, ForeignKey("users.pk"))
    member = relationship("User", back_populates="answers")

    anon_member_pk = Column(Integer, ForeignKey("quiz_anon_users.pk"))
    anon_member = relationship("QuizAnonUser", back_populates="answers")

    step_option_pk = Column(Integer, ForeignKey("step_options.pk"))
    step_option = relationship("StepOption", back_populates="answers")

    time_to_estimate = Column(Integer, nullable=False)
    rank = Column(Integer, nullable=True)
