from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean

from core.database import Base
from core.manager import BaseManagerMixin
from core.models import Timestamped


class Event(Timestamped, BaseManagerMixin):

    __tablename__ = "events"

    pk = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    owner_pk = Column(Integer, ForeignKey("users.pk"))
    owner = relationship("User", back_populates="events")

    questions = relationship(
        "Question", back_populates="event", order_by="Question.likes_count.desc()"
    )

    __mapper_args__ = {
        "polymorphic_identity": "events",
    }


likes_table = Table(
    "likes",
    Base.metadata,
    Column("user_pk", Integer, ForeignKey("users.pk"), nullable=True),
    Column("question_pk", Integer, ForeignKey("questions.pk"), nullable=True),
)


class Question(Timestamped, BaseManagerMixin):

    __tablename__ = "questions"

    pk = Column(Integer, primary_key=True, index=True)
    body = Column(String, nullable=False)

    event_pk = Column(Integer, ForeignKey("events.pk"), nullable=True)
    event = relationship("Event", back_populates="questions")

    author_pk = Column(Integer, ForeignKey("users.pk"), nullable=True)
    author = relationship("User", back_populates="questions")

    answered = Column(Boolean, default=False)

    likes_count = Column(Integer, default=0)
    likes = relationship(
        "User", secondary=likes_table, back_populates="liked_questions"
    )


class Poll(Timestamped, BaseManagerMixin):

    __tablename__ = "polls"

    pk = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    multiply_votes = Column(Boolean, default=False)
    allowed_votes = Column(Integer, default=1)

    owner_pk = Column(Integer, ForeignKey("users.pk"))
    owner = relationship("User", back_populates="polls")

    options = relationship(
        "Option", back_populates="poll", order_by="Option.created.desc()"
    )
    votes = relationship("Vote", back_populates="poll", order_by="Vote.created.desc()")

    @property
    def rating(self):
        ratings = {}
        return ratings


class Option(Timestamped, BaseManagerMixin):

    __tablename__ = "options"

    pk = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    poll_pk = Column(Integer, ForeignKey("polls.pk"))
    poll = relationship("Poll", back_populates="options")

    votes = relationship(
        "Vote", back_populates="option", order_by="Vote.created.desc()"
    )


class Vote(Timestamped, BaseManagerMixin):

    __tablename__ = "votes"

    pk = Column(Integer, primary_key=True, index=True)

    poll_pk = Column(Integer, ForeignKey("polls.pk"))
    poll = relationship("Poll", back_populates="votes")

    owner_pk = Column(Integer, ForeignKey("users.pk"))
    owner = relationship("User", back_populates="votes")

    owner_host = Column(String, nullable=True)

    option_pk = Column(Integer, ForeignKey("options.pk"))
    option = relationship("Option", back_populates="votes")
