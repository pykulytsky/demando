from typing import List, Type, Union

from fastapi import Depends
from sqlalchemy import MetaData
from sqlalchemy.orm import Session

from core.database import Base
from core.exceptions import ImproperlyConfigured, ObjectDoesNotExists

from .database import get_db


class BaseManager:
    def __init__(self, klass: Type, db: Session = Depends(get_db)) -> None:
        if not issubclass(klass, Base):
            raise ImproperlyConfigured(f"Type {klass.__name__} is not suported.")
        self.model = klass

        self.db = db

    def create(self, disable_check: bool = False, **fields):
        if not disable_check:
            self.check_fields(**fields)
        instance = self.model(**fields)

        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)

        return instance

    def delete(self, instance):
        if not isinstance(instance, self.model):
            raise TypeError(f"Instance must be {str(self.model)} not {type(instance)}")
        self.db.delete(instance)
        self.db.commit()

    def all(
        self,
        skip: int = 0,
        limit: int = 100,
        order_by: str = "created",
        desc: bool = False,
    ) -> List[Type]:
        try:
            if desc:
                return (
                    self.db.query(self.model)
                    .order_by(getattr(self.model, order_by).desc())
                    .offset(skip)
                    .limit(limit)
                    .all()
                )
            return (
                self.db.query(self.model)
                .order_by(getattr(self.model, order_by))
                .offset(skip)
                .limit(limit)
                .all()
            )
        except AttributeError:
            return self.db.query(self.model).offset(skip).limit(limit).all()

    def get(self, **fields) -> Type:
        self.check_fields(**fields)

        expression = [getattr(self.model, k) == fields[k] for k in fields.keys()]

        instance = self.db.query(self.model).filter(*expression).first()
        if instance:
            return instance

        raise ObjectDoesNotExists(
            f"No {self.model.__name__.lower()} with such parameters."
        )

    def update(self, pk, **updated_fields):
        self.check_fields(**updated_fields)
        instance = self.get(pk=pk)

        for field in updated_fields:
            setattr(instance, field, updated_fields[field])

        self.db.commit()
        self.db.refresh(instance)

        return instance

    def filter(self, **fields):
        self.check_fields(**fields)

        expression = [getattr(self.model, k) == fields[k] for k in fields.keys()]

        return self.db.query(self.model).filter(*expression).all()

    def get_or_false(self, **fields) -> Union[Type, bool]:
        try:
            instance = self.get(**fields)
            return instance
        except ObjectDoesNotExists:
            return False

    def exists(self, **fields):
        try:
            self.get(**fields)
            return True
        except ObjectDoesNotExists:
            return False

    def _get_model_fields(self) -> List[str]:
        fields = []

        for field in dir(self.model):
            if not field.startswith("_"):
                if not callable(getattr(self.model, field)) and not isinstance(
                    getattr(self.model, field), MetaData
                ):  # noqa
                    fields.append(field)

        return fields

    def check_fields(self, **fields):
        for field in fields.keys():
            if field not in self._get_model_fields():
                raise ValueError(
                    f"Field {field} is not suported, suported fields: {self._get_model_fields()}"
                )  # noqa

    def refresh(self, instance):
        self.db.commit()
        self.db.refresh(instance)

        return instance


class BaseManagerMixin:
    @classmethod
    def manager(cls, db):
        return BaseManager(cls, db)
