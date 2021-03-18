from .exceptions import JwtTokenError
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from passlib.hash import pbkdf2_sha256
import jwt
from datetime import datetime
from datetime import timedelta

from base import settings

from base.database import Base
from jwt.exceptions import InvalidAlgorithmError, InvalidSignatureError
from questions.models import likes_table
from base.manager import BaseManagerModel

from typing import Optional


class Role(Base, BaseManagerModel):

    __tablename__ = 'roles'

    pk = Column(Integer, primary_key=True, index=True)
    verbose = Column(String)

    users = relationship('User', back_populates="role")


class User(Base, BaseManagerModel):

    __tablename__ = 'users'

    pk = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)

    password = Column(String)
    email = Column(String, unique=True)

    is_superuser = Column(Boolean, default=False, nullable=True)

    role_pk = Column(Integer, ForeignKey('roles.pk'))
    role = relationship("Role", back_populates="users")

    events = relationship('Event', back_populates='owner')
    questions = relationship('Question', back_populates='author')
    liked_questions = relationship(
        'Question', secondary=likes_table, back_populates="likes"
    )

    def __init__(
        self,
        username: str,
        password: str,
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
    ) -> None:
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

        print(f'{self.__module__=}')
        print(f'{self.__class__=}')

        self.set_password(password)

    def set_password(self, password: str) -> str:
        self.password = pbkdf2_sha256.using(
            salt=bytes(settings.SECRET_KEY.encode('utf-8'))
        ).hash(password)
        return self.password

    def verify_password(self, password: str):
        return pbkdf2_sha256.using(
            salt=bytes(settings.SECRET_KEY.encode('utf-8'))
        ).verify(password, self.password)

    @property
    def token(self) -> str:
        return self.generate_jwt_token()

    def generate_jwt_token(self) -> str:
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

    def __str__(self) -> str:
        return f'<User: {self.username}>'
