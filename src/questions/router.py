from auth.models import User
from base.router import CrudRouter
from pydantic import BaseModel

from fastapi import Depends
from base.database import Base, get_db, engine
from sqlalchemy.orm import Session
from typing import Dict, Optional, List, Type
from base.utils import get_class_by_table

from auth.backend import JWTAuthentication, authenticate


class ItemRouter(CrudRouter):
    def __init__(
        self,
        model,
        get_schema: BaseModel,
        create_schema: BaseModel,
        update_schema: BaseModel = None,
        db: Session = Depends(get_db),
        prefix: Optional[str] = None,
        tags: Optional[List] = [],
        auth_backend: Type = JWTAuthentication,
        add_create_route: bool = False,
        *args,
        **kwargs
    ) -> None:
        self.auth_backend = auth_backend

        super().__init__(
            model,
            get_schema,
            create_schema,
            update_schema=update_schema,
            db=db,
            prefix=prefix,
            tags=tags,
            add_create_route=add_create_route,
            *args,
            **kwargs
        )

        super().add_api_route(
            '/',
            self._create(),
            methods=['POST'],
            response_model=self.get_schema,
            dependencies=[Depends(get_db)],
            summary=f"Create {self.model.__name__}",
            status_code=201
        )

    def _create(self):
        async def route(
            create_schema: self.create_schema,
            db: Session = Depends(get_db),
            user: User = Depends(authenticate)
        ):
            print(self.get_create_data(
                    create_schema=create_schema,
                    user=user,
                    db=db
                ))

            instance = self.model.manager(db).create(
                **self.get_create_data(
                    create_schema=create_schema,
                    user=user,
                    db=db
                )
            )
            return instance

        return route

    def _get_schemas_diff(self, exclude: Optional[List] = None) -> List:
        """Check get and create schema and return array of fields that are different"""
        fields = []

        for field in self.create_schema.__annotations__:
            try:
                if self.get_schema.__annotations__[field] != self.create_schema.__annotations__[field]:
                    if (exclude and field not in exclude) or not exclude:
                        fields.append(field)
            except KeyError:
                if (exclude and field not in exclude) or not exclude:
                    fields.append(field)

        return fields

    def _get_schema_diff_models(self) -> List:
        Base.metadata.create_all(engine)

        fields = self._get_schemas_diff()
        models = list()

        for i in range(len(fields)):
            fields[i] = fields[i] + 's'
            if fields[i] == 'authors' or fields[i] == 'owners':
                fields[i] = 'users'

            models.append(get_class_by_table(Base, fields[i]))

        return models

    def _get_schema_diff_models_exclude_user(self) -> List:
        Base.metadata.create_all(engine)

        fields = self._get_schemas_diff(exclude=['user', 'owner', 'author'])

        models = list()

        for i in range(len(fields)):
            fields[i] = fields[i] + 's'
            models.append(get_class_by_table(Base, fields[i]))

        return models

    def find_user_field(self):
        pass

    def get_create_data(self, create_schema, user, db) -> Dict:
        data = {}

        model_fields = self._get_schemas_diff(
            exclude=['user', 'owner', 'author']
        )
        models = self._get_schema_diff_models_exclude_user()

        for field in create_schema.__dict__.keys():
            if field in model_fields:
                if hasattr(models[model_fields.index(field)], 'manager'):
                    data.update({
                        field: models[model_fields.index(field)].manager(db).get(pk=getattr(create_schema, field))
                    })
            else:
                data.update({
                    field: create_schema.__dict__[field]
                })

        for user_field in ['user', 'author', 'owner']:
            if hasattr(self.model, user_field):
                data.update({user_field: user})

        return data
