from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean
from base.database import Base


class Event(Base):

    __tablename__ = 'events'

    pk = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    owner_pk = Column(Integer, ForeignKey('users.pk'))
    owner = relationship('User', back_populates='events')

    questions = relationship('Question', back_populates='event')


likes_table = Table('likes', Base.metadata,
                    Column(
                        'user_pk',
                        Integer,
                        ForeignKey('users.pk'),
                        nullable=True),
                    Column(
                        'question_pk',
                        Integer,
                        ForeignKey('questions.pk'),
                        nullable=True)
                    )


class Question(Base):

    __tablename__ = 'questions'

    pk = Column(Integer, primary_key=True, index=True)
    body = Column(String, nullable=False)

    event_pk = Column(Integer, ForeignKey('events.pk'), nullable=True)
    event = relationship('Event', back_populates="questions")

    author_pk = Column(Integer, ForeignKey('users.pk'), nullable=True)
    author = relationship('User', back_populates='questions')

    answered = Column(Boolean, default=False)

    likes_count = Column(Integer, default=0)
    likes = relationship(
        'User', secondary=likes_table, back_populates="liked_questions"
    )
