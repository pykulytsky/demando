from .exceptions import JwtTokenError
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

import jwt
from datetime import datetime
from datetime import timedelta

from demando.base import settings

from demando.base.database import Base
from jwt.exceptions import InvalidAlgorithmError, InvalidSignatureError
from demando.questions.models import Event, Poll, Question, UserLikes, Vote
from .manager import AuthManagerModel

from typing import Optional

from demando.base.database import db


class Role(db.Model, AuthManagerModel):

    __tablename__ = 'roles'

    pk = db.Column(db.Integer(), primary_key=True, index=True)
    verbose = db.Column(db.String())

    @property
    async def users(self):
        return await User.query.where(User.role_pk == self.pk).gino.all()


class User(db.Model, AuthManagerModel):

    __tablename__ = 'users'

    pk = db.Column(db.Integer(), primary_key=True, index=True)
    username = db.Column(db.String(), unique=True)
    first_name = db.Column(db.String(), nullable=True)
    last_name = db.Column(db.String(), nullable=True)
    age = db.Column(db.Integer(), nullable=True)

    password = db.Column(db.String())
    email = db.Column(db.String(), unique=True)

    is_superuser = db.Column(db.Boolean(), default=False, nullable=True)

    role_pk = db.Column(db.Integer(), db.ForeignKey('roles.pk'))
    role = relationship("Role", back_populates="users")

    @property
    async def role(self):
        return await Role.get(self.role_pk)

    @property
    async def polls(self):
        return await Poll.query.where(Poll.owner_pk == self.pk).gino.all()

    @property
    async def votes(self):
        return await Vote.query.where(Vote.owner_pk == self.pk).gino.all()

    @property
    async def events(self):
        return await Event.query.where(Event.owner_pk == self.pk).gino.all()

    @property
    async def quetions(self):
        return await Question.query.where(Question.owner_pk == self.pk).gino.all()

    @property
    async def liked_questions(self):
        return await UserLikes.query.where(UserLikes.user_pk == self.pk).gino.all()


    @property
    async def token(self) -> str:
        return await self.generate_jwt_token()

    async def generate_jwt_token(self) -> str:
        period = datetime.now() + timedelta(days=60)
        try:
            token = jwt.encode({
                'pk': self.pk,
                'exp': period.timestamp(),
                'is_superuser': int(self.is_superuser)
            }, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        except (InvalidAlgorithmError, InvalidSignatureError):
            raise JwtTokenError("Error occured, while generating JWT token.")

        return token.decode('utf-8')

    async def __str__(self) -> str:
        return f'<User: {self.username}>'
