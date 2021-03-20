from typing import Type
from auth.exceptions import WrongLoginCredentials
from base import settings
from base.exceptions import ObjectDoesNotExists
from base.manager import BaseManager, BaseManagerModel

from passlib.hash import pbkdf2_sha256

from . import schemas


class AuthManager(BaseManager):

    def create_user(self, user_schema: schemas.UserCreate):
        fields = user_schema.__dict__
        self.check_fields(**fields)
        fields['password'] = self.set_password(fields['password'])

        instance = super().create(
            disable_check=True, **fields
        )

        self.refresh(instance)

        return instance

    def set_password(self, passwd: str) -> str:
        password = self._hasher().hash(passwd)
        return password

    @staticmethod
    def verify_password(password: str, instance: Type) -> bool:
        return AuthManager._hasher().verify(password, instance.password)

    @staticmethod
    def _hasher():
        return pbkdf2_sha256.using(
            salt=bytes(settings.SECRET_KEY.encode('utf-8'))
        )

    def login(self, login_schema: schemas.UserLogin):
        try:
            user = self.get(email=login_schema.email)
            if self.verify_password(login_schema.password, user):
                return user
            else:
                raise WrongLoginCredentials("Password didnt match.")
        except ObjectDoesNotExists:
            raise WrongLoginCredentials("No user with such email was found.")


class AuthManagerModel(BaseManagerModel):
    @classmethod
    def manager(cls, db):
        return AuthManager(cls, db)
