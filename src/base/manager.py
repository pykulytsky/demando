from typing import List, Type

from sqlalchemy.orm import Session
from base.database import SessionLocal


class BaseManager():
    def __init__(self, model: Type, db: Session = SessionLocal()) -> None:
        self.model = model
        self.db = db

    def create(self, instance):
        if not isinstance(instance, self.model):
            raise TypeError(
                f"Instance must be {str(self.model)} not {type(instance)}"
            )
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

    def all(self) -> List[Type]:
        return self.db.query(self.model).all()
