import uuid
from datetime import datetime, timedelta

import jwt
from jwt.exceptions import InvalidAlgorithmError, InvalidSignatureError
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import settings
from core.database import Base
from core.manager import BaseManagerMixin
from questions.models import likes_table
from quiz.models import member_table

from .exceptions import JwtTokenError
from .manager import AuthManagerMixin


class Role(Base, AuthManagerMixin):

    __tablename__ = "roles"

    pk = Column(Integer, primary_key=True, index=True)
    verbose = Column(String)

    users = relationship("User", back_populates="role")


class User(Base, AuthManagerMixin):

    __tablename__ = "users"

    pk = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)

    password = Column(String)
    email = Column(String, unique=True)
    country = Column(String, nullable=True)
    avatar = Column(String, nullable=True)

    active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False, nullable=True)

    role_pk = Column(Integer, ForeignKey("roles.pk"))
    role = relationship("Role", back_populates="users")

    events = relationship("Event", back_populates="owner")
    polls = relationship("Poll", back_populates="owner")
    votes = relationship("Vote", back_populates="owner")
    questions = relationship("Question", back_populates="author")
    quizzes = relationship("Quiz", secondary=member_table, back_populates="owner")
    answers = relationship("Answer", back_populates="member")
    # links = relationship("SocialMediaLink", back_populates="profile")

    liked_questions = relationship(
        "Question", secondary=likes_table, back_populates="likes"
    )

    verification_code = Column(UUID(as_uuid=True), default=uuid.uuid4())
    email_verified = Column(Boolean, default=False)

    @property
    def token(self) -> str:
        return self.generate_jwt_token()

    def generate_jwt_token(self) -> str:
        period = datetime.now() + timedelta(days=60)
        try:
            token = jwt.encode(
                {
                    "pk": self.pk,
                    "exp": period.timestamp(),
                    "is_superuser": int(self.is_superuser),
                },
                settings.SECRET_KEY,
                algorithm=settings.ALGORITHM,
            )

        except (InvalidAlgorithmError, InvalidSignatureError):
            raise JwtTokenError("Error occured, while generating JWT token.")

        return token.decode("utf-8")

    def __str__(self) -> str:
        return f"<User: {self.username}>"


class SocialMediaLink(Base, BaseManagerMixin):

    __tablename__ = "links"

    pk = Column(Integer, primary_key=True, index=True)
    link = Column(String, nullable=False)
    social_media = Column(String, nullable=False)
    # profile = Column(Integer, ForeignKey("users.pk"))
    # profile_pk = relationship("User", back_populates="links")
