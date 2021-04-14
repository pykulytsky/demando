from typing import Any, Iterable, Optional, Type
from tortoise.models import MODEL, Model
from tortoise import fields

from auth import schemas
from . import validators
from base import settings

import jwt
from jwt.exceptions import InvalidAlgorithmError, InvalidSignatureError
from .exceptions import JwtTokenError, WrongLoginCredentials

from datetime import datetime
from datetime import timedelta
import uuid

from passlib.hash import pbkdf2_sha256


class User(Model):

    id = fields.IntField(pk=True)

    username = fields.CharField(max_length=256, unique=True)
    first_name = fields.CharField(max_length=256, null=True)
    last_name = fields.CharField(max_length=256, null=True)

    age = fields.IntField(null=True)

    password = fields.CharField(max_length=256)
    email = fields.CharField(
        max_length=256,
        validators=[validators.EmailValidator()]
    )

    is_superuser = fields.BooleanField(default=False)
    is_active = fields.BooleanField(default=True)

    role = fields.ForeignKeyField('auth.Role', related_name='users', null=True)

    created = fields.DatetimeField(auto_now=True)
    updated = fields.DatetimeField(auto_now_add=True)

    verification_code = fields.UUIDField(default=uuid.uuid4())

    @classmethod
    async def create(cls: Type[MODEL], **kwargs: Any) -> MODEL:
        if kwargs.get('first_name', False):
            kwargs['first_name'] = kwargs['first_name'].capitalize()
        if kwargs.get('last_name', False):
            kwargs['last_name'] = kwargs['last_name'].capitalize()

        kwargs['password'] = await cls.set_password(kwargs['password'])

        return await super().create(**kwargs)

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'

    @staticmethod
    async def set_password(passwd: str) -> str:
        password = User._hasher().hash(passwd)
        return password

    @staticmethod
    def verify_password(password: str, instance: Type) -> bool:
        return User._hasher().verify(password, instance.password)

    @staticmethod
    def _hasher():
        return pbkdf2_sha256.using(
            salt=bytes(settings.SECRET_KEY.encode('utf-8'))
        )

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

    @staticmethod
    async def login(login_schema: schemas.UserLogin):
        user = await User.get(email=login_schema.email)
        if User.verify_password(login_schema.password, user):
            return user
        else:
            raise WrongLoginCredentials("Password didnt match.")

    def __str__(self) -> str:
        return f'<User: {self.username}>'

    class Meta:
        table = 'users'


class Role(Model):
    id = fields.IntField(pk=True)
    verbose = fields.CharField(max_length=128)
