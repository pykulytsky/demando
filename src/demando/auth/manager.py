from typing import Type
from .exceptions import WrongLoginCredentials
from demando.base import settings
from demando.base.exceptions import ObjectDoesNotExists
from demando.base.manager import BaseManager, BaseManagerModel

from passlib.hash import pbkdf2_sha256

from . import schemas


class AuthManager(BaseManager):

    async def create_user(self, user_schema: schemas.UserCreate):
        fields = user_schema.__dict__
        await self.check_fields(**fields)
        fields['password'] = self.set_password(fields['password'])

        instance = await self.model.create(**fields)

        return instance

    async def set_password(self, passwd: str) -> str:
        password = self._hasher().hash(passwd)
        return password

    @staticmethod
    async def verify_password(password: str, instance: Type) -> bool:
        return AuthManager._hasher().verify(password, instance.password)

    @staticmethod
    def _hasher():
        return pbkdf2_sha256.using(
            salt=bytes(settings.SECRET_KEY.encode('utf-8'))
        )

    async def login(self, login_schema: schemas.UserLogin):
        user = await self.get(email=login_schema.email)
        if user:
            if await self.verify_password(login_schema.password, user):
                return user
            else:
                raise WrongLoginCredentials("Password didnt match.")
        else:
            raise WrongLoginCredentials("No user with such email was found.")


class AuthManagerModel(BaseManagerModel):
    @classmethod
    def manager(cls):
        return AuthManager(cls)
