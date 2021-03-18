from typing import Type
from base import settings
from base.manager import BaseManager
from .models import User

from passlib.hash import pbkdf2_sha256


class AuthManager(BaseManager):

    def create_user(self, **fields):
        self.check_fields(**fields)

        instance = super(self, BaseManager).create(
            disable_check=True, **fields
        )
        self.set_password(instance)
        self.refresh(instance)

    def set_password(self, instance: Type) -> str:
        passwd = instance.password

        instance.password = pbkdf2_sha256.using(
            salt=bytes(settings.SECRET_KEY.encode('utf-8'))
        ).hash(passwd)
        return instance.password

    def verify_password(self, password: str, instance: Type):
        return pbkdf2_sha256.using(
            salt=bytes(settings.SECRET_KEY.encode('utf-8'))
        ).verify(password, instance.password)
