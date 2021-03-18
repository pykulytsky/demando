from typing import Callable, List, Type, Union

from sqlalchemy.orm import Session
from base.database import SessionLocal
from base.exceptions import ObjectDoesNotExists


class BaseManager():
    def __init__(self, klass: Type, db: Session = SessionLocal()) -> None:
        self.model = klass

        self.db = db

    def create(self, disable_check: bool = False, **fields):
        if disable_check:
            self.check_fields(**fields)

        instance = self.model(**fields)

        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)

        return instance

    def delete(self, instance):
        if not isinstance(instance, self.model):
            raise TypeError(
                f"Instance must be {str(self.model)} not {type(instance)}"
            )
        self.db.delete(instance)
        self.db.commit()
        self.db.refresh(instance)

        return instance

    def all(self, skip: int = 0, limit: int = 100) -> List[Type]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def get(self, **fields) -> Type:
        self.check_fields(**fields)

        expression = [
            getattr(self.model, k) == fields[k] for k in fields.keys()
        ]

        instance = self.db.query(self.model).filter(*expression).first()
        if instance:
            return instance

        raise ObjectDoesNotExists(
            f"No {self.model.__name__.lower()} with such parameters."
        )

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
            if not field.startswith('_'):
                if not isinstance(getattr(self.model, field), Callable):
                    fields.append(field)

        return fields

    def check_fields(self, **fields):
        for field in fields.keys():
            if field not in self._get_model_fields():
                raise ValueError(
                    f"Field {field} is not suported, suported fields: {self._get_model_fields()}")

    def refresh(self, instance):
        self.db.commit()
        self.db.refresh(instance)

        return instance


class BaseManagerModel():
    @classmethod
    def manager(cls):
        return BaseManager(cls)
