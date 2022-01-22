from typing import Type

from fastapi import Depends
from base.database import get_db
from sqlalchemy.orm import Session

from base.manager import BaseManager


class ItemManager(BaseManager):
    def __init__(
        self,
        klass: Type,
        user_model: Type,
        db: Session = Depends(get_db),
    ) -> None:
        self.user_model = user_model
        super().__init__(klass, db=db)

    def create(self, **fields):
        data = {
            'name': fields['name']
        }
        if fields.get('author', False):
            data.update({
                'author': self.user_model.manager(
                    self.db
                ).get(pk=fields['author'])
            })
        if fields.get('owner', False):
            data.update({
                'owner': self.user_model.manager(
                    self.db
                ).get(pk=fields['owner'])
            })

        return super().create(disable_check=True, **data)


class ItemManagerModel():
    @classmethod
    def manager(cls, db):
        return ItemManager(cls, db)
