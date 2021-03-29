from typing import List, Type, Union

from sqlalchemy.orm import Session
from sqlalchemy import MetaData
from .database import Base
from .exceptions import ObjectDoesNotExists, ImproperlyConfigured

from fastapi import Depends
from .database import get_db


class BaseManager():
    def __init__(self, klass: Type) -> None:
        self.model = klass

    async def create(self, disable_check: bool = False, **fields):
        if not disable_check:
            await self.check_fields(**fields)

        return await self.model.create(**fields)

    async def delete(self, instance):
        if not isinstance(instance, self.model):
            raise TypeError(
                f"Instance must be {str(self.model)} not {type(instance)}"
            )
        self.db.delete(instance)
        self.db.commit()
        self.db.refresh(instance)

        return instance

    async def all(self, skip: int = 0, limit: int = 100) -> List[Type]:
        return await self.model.query.offset(skip).limit(limit).gino.all()

    async def get(self, **fields) -> Type:
        await self.check_fields(**fields)

        expression = [
            getattr(self.model, k) == fields[k] for k in fields.keys()
        ]

        instance = await self.model.query.where(*expression).gino.first()
        if instance:
            return instance

        raise ObjectDoesNotExists("Object not found.")

    async def filter(self, **fields):
        await self.check_fields(**fields)

        expression = [
            getattr(self.model, k) == fields[k] for k in fields.keys()
        ]

        return await self.model.query.where(*expression).gino.all()

    async def get_or_false(self, **fields) -> Union[Type, bool]:
        try:
            instance = await self.get(**fields)
            return instance
        except ObjectDoesNotExists:
            return False

    async def exists(self, **fields):
        try:
            await self.get(**fields)
            return True
        except ObjectDoesNotExists:
            return False

    async def _get_model_fields(self) -> List[str]:
        fields = []

        for field in dir(self.model):
            if not field.startswith('_'):
                if not callable(getattr(self.model, field)) and not isinstance(getattr(self.model, field), MetaData): # noqa
                    fields.append(field)

        return fields

    async def check_fields(self, **fields):
        for field in fields.keys():
            if field not in await self._get_model_fields():
                raise ValueError(f"Field {field} is not suported, suported fields: {await self._get_model_fields()}") # noqa


class BaseManagerModel():
    @classmethod
    def manager(cls):
        return BaseManager(cls)
