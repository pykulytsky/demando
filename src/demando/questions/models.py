from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean
from demando.base.database import Base

from demando.base.manager import BaseManagerModel
from demando.base.database import db


class Event(db.Model, BaseManagerModel):

    __tablename__ = 'events'

    pk = db.Column(Integer(), primary_key=True, index=True)
    name = db.Column(db.String(), unique=True)

    owner_pk = db.Column(db.Integer(), ForeignKey('users.pk'))

    @property
    async def owner(self):
        from demando.auth.models import User
        return await User.get(self.owner_pk)

    @property
    async def questions(self):
        return await Question.query.where(Question.event_pk == self.pk).gino.all()


class UserLikes(db.Model):

    __tablename__ = 'user_likes'

    user_pk = db.Column(db.Integer(), ForeignKey('users.pk'), nullable=True)
    question_pk = db.Column(db.Integer(), ForeignKey('questions.pk'), nullable=True)


class Question(db.Model, BaseManagerModel):

    __tablename__ = 'questions'

    pk = db.Column(db.Integer(), primary_key=True, index=True)
    body = db.Column(db.String(), nullable=False)

    event_pk = db.Column(db.Integer(), db.ForeignKey('events.pk'), nullable=True)
    event = relationship('Event', back_populates="questions")

    author_pk = db.Column(db.Integer(), db.ForeignKey('users.pk'), nullable=True)
    author = relationship('User', back_populates='questions')

    @property
    async def author(self):
        from demando.auth.models import User

        return await User.get(self.author_pk)

    answered = db.Column(db.Boolean(), default=False)

    likes_count = db.Column(db.Integer(), default=0)

    @property
    async def likes(self):
        return await UserLikes.query.where(UserLikes.question_pk == self.pk).gino.all()


class Poll(db.Model, BaseManagerModel):

    __tablename__ = 'polls'

    pk = db.Column(db.Integer(), primary_key=True, index=True)
    name = db.Column(db.String(), nullable=False)

    owner_pk = db.Column(db.Integer(), db.ForeignKey('users.pk'))

    @property
    async def owner(self):
        from demando.auth.models import User
        return await User.get(self.owner_pk)

    @property
    async def options(self):
        return await Option.query.where(Option.poll_pk == self.pk).gino.all()

    @property
    async def votes(self):
        return await Vote.query.where(Vote.poll_pk == self.pk).gino.all()


class Option(db.Model, BaseManagerModel):

    __tablename__ = 'options'

    pk = db.Column(db.Integer(), primary_key=True, index=True)
    name = db.Column(db.String(), nullable=False)

    poll_pk = db.Column(db.Integer(), db.ForeignKey('polls.pk'))

    @property
    async def poll(self):
        return await Poll.get(self.poll_pk)

    @property
    async def votes(self):
        return await Vote.query.where(Vote.option_pk == self.pk).gino.all()


class Vote(db.Model, BaseManagerModel):

    __tablename__ = 'votes'

    pk = db.Column(db.Integer(), primary_key=True, index=True)

    poll_pk = db.Column(db.Integer(), db.ForeignKey('polls.pk'))

    @property
    async def poll(self):
        return await Poll.get(self.poll_pk)

    owner_pk = db.Column(db.Integer(), db.ForeignKey('users.pk'))

    @property
    async def owner(self):
        from demando.auth.models import User
        return await User.get(self.owner_pk)

    option_pk = db.Column(db.Integer(), db.ForeignKey('options.pk'))

    @property
    async def option(self):
        return await Option.get(self.option_pk)
