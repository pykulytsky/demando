import uuid
from datetime import datetime, timedelta

import jwt
from jwt.exceptions import InvalidAlgorithmError, InvalidSignatureError
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from base import settings
from base.database import Base
from questions.models import likes_table

from .exceptions import JwtTokenError
from .manager import AuthManagerModel


class Role(Base, AuthManagerModel):

    __tablename__ = "roles"

    pk = Column(Integer, primary_key=True, index=True)
    verbose = Column(String)

    users = relationship("User", back_populates="role")


class User(Base, AuthManagerModel):

    __tablename__ = "users"

    pk = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)

    password = Column(String)
    email = Column(String, unique=True)

    active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False, nullable=True)

    role_pk = Column(Integer, ForeignKey("roles.pk"))
    role = relationship("Role", back_populates="users")

    events = relationship("Event", back_populates="owner")
    polls = relationship("Poll", back_populates="owner")
    votes = relationship("Vote", back_populates="owner")
    questions = relationship("Question", back_populates="author")

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
