import typing
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Type

from fastapi import Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from auth.backend import JWTAuthentication, authenticate
from auth.models import User
from core import settings
from core.database import Base, engine, get_db
from core.router import CrudRouter
from core.utils import get_class_by_table
from questions.models import Event, Question
from tasks.mails import notify_event_statistic


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
        **kwargs,
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
            **kwargs,
        )

        super().add_api_route(
            "/",
            self._create(),
            methods=["POST"],
            response_model=self.get_schema,
            dependencies=[Depends(get_db)],
            summary=f"Create {self.model.__name__}",
            status_code=201,
        )

    def _create(self):
        async def route(
            create_schema: self.create_schema,
            db: Session = Depends(get_db),
            user: User = Depends(authenticate),
        ):
            if (
                user.email_verified
                or self.model == Question
                or settings.ALLOW_EVERYONE_CREATE_ITEMS
            ):  # noqa
                instance = self.model.manager(db).create(
                    **self.get_create_data(
                        create_schema=create_schema, user=user, db=db
                    )
                )
                if instance:
                    if self.model == Event:
                        notify_event_statistic.apply_async(
                            (instance.pk,), eta=datetime.utcnow() + timedelta(days=7)
                        )
                    return instance
            else:
                raise HTTPException(
                    status_code=403, detail="User must have verified email"
                )

        return route

    def _get_schemas_diff(self, exclude: Optional[List] = None) -> List:
        """Check get and create schema and return array of fields that are different"""  # noqa
        fields = []
        for field in self.create_schema.__annotations__:
            try:
                if (
                    self.get_schema.__annotations__[field]
                    != self.create_schema.__annotations__[field]
                ):  # noqa
                    if (exclude and field not in exclude) or not exclude:
                        if (
                            self.create_schema.__annotations__[field]
                            != typing.Union[str, None]
                        ):
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
            if fields[i] == "quiz":
                fields[i] = "quizzes"
            else:
                fields[i] = fields[i] + "s"
                if fields[i] == "authors" or fields[i] == "owners":
                    fields[i] = "users"

            models.append(get_class_by_table(Base, fields[i]))

        return models

    def _get_schema_diff_models_exclude_user(self) -> List:
        Base.metadata.create_all(engine)

        fields = self._get_schemas_diff(exclude=["user", "owner", "author"])
        models = list()
        for i in range(len(fields)):
            if fields[i] == "quiz":
                fields[i] = "quizzes"
            else:
                fields[i] = fields[i] + "s"

            models.append(get_class_by_table(Base, fields[i]))
        return models

    def find_user_field(self):
        pass

    def get_create_data(self, create_schema, user, db) -> Dict:
        data = {}

        model_fields = self._get_schemas_diff(exclude=["user", "owner", "author"])
        models = self._get_schema_diff_models_exclude_user()

        for field in create_schema.__dict__.keys():
            if field in model_fields:
                if hasattr(models[model_fields.index(field)], "manager"):
                    data.update(
                        {
                            field: models[model_fields.index(field)]
                            .manager(db)
                            .get(pk=getattr(create_schema, field))  # noqa
                        }
                    )
            else:
                data.update({field: create_schema.__dict__[field]})

        for user_field in ["user", "author", "owner"]:
            if hasattr(self.model, user_field):
                data.update({user_field: user})

        return data
