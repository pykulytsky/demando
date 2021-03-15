from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from base.database import Base


class Event(Base):

    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship('User', back_populates='events')

    questions = relationship('Question', back_populates='event')


likes_table = Table('likes', Base.metadata,
                    Column('user_id', Integer, ForeignKey('users.id'), nullable=True),
                    Column('question_id', Integer, ForeignKey('questions.id'), nullable=True)
                    )


class Question(Base):

    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, index=True)
    body = Column(String, nullable=False)

    event_id = Column(Integer, ForeignKey('events.id'), nullable=True)
    event = relationship('Event', back_populates="questions")

    author_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    author = relationship('User', back_populates='questions')

    likes_count = Column(Integer, default=0)
    likes = relationship(
        'User', secondary=likes_table, back_populates="liked_questions"
    )
