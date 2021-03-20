from typing import Callable, List, Optional

from .exceptions import ImproperlyConfigured, ObjectDoesNotExists
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from .database import get_db

from pydantic import BaseModel


class BaseCrudRouter(APIRouter):
    """Base router that implements basic CRUD operations(.get(), .get_all(), .create(), .delete())"""
    model = None
    create_schema = None
    get_schema = None

    def __init__(
        self,
        model,
        get_schema: BaseModel,
        create_schema: BaseModel,
        update_schema: BaseModel = None,
        db: Session = Depends(get_db),
        prefix: Optional[str] = None,
        tags: Optional[List] = [],
        *args,
        **kwargs
    ) -> None:
        if not hasattr(model, 'manager'):
            raise AttributeError(f"Model {model.__name__} not suported, model must have a 'manager' field.")

        self.model = model

        self.get_schema = get_schema
        self.create_schema = create_schema
        self.update_schema = update_schema

        self.prefix = prefix
        if not prefix:
            self.prefix = '/' + self.model.__name__.lower()
        self.tags = tags

        if not all([
            self.model, self.create_schema, self.get_schema
        ]):
            raise ImproperlyConfigured("Please redifine fields model, create_schema, get_schema in your subclass")

        super().__init__(prefix=prefix, tags=tags, *args, **kwargs)

        super().add_api_route(
            '/',
            self._get_all,
            response_model=List[self.get_schema],
            dependencies=[Depends(get_db)],
            summary=f"Get all {self.model.__name__}`s"
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
        super().add_api_route(
            '/{pk}',
            self._get(),
            methods=['GET'],
            response_model=self.get_schema,
            dependencies=[Depends(get_db)],
            summary=f"Get {self.model.__name__}"
        )
        super().add_api_route(
            '/{pk}',
            self._update(),
            methods=['PATCH'],
            response_model=self.get_schema,
            dependencies=[Depends(get_db)],
            summary=f"Update {self.model.__name__}"
        )
        super().add_api_route(
            '/{pk}',
            self._delete(),
            methods=['DELETE'],
            response_model=self.get_schema,
            dependencies=[Depends(get_db)],
            summary=f"Delete {self.model.__name__}"
        )

    async def _get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
    ) -> Callable:
        @self.get('/', response_model=List[self.get_schema])
        async def _get_all(
            skip: int = 0,
            limit: int = 100,
            db: Session = Depends(get_db)
        ):
            return self.model.manager(db).all(skip, limit)

        return await _get_all(skip, limit, db)

    def _create(self) -> Callable:
        async def route(instance_create_schema: self.create_schema, db: Session = Depends(get_db)):
            return self.model.manager(db).create(instance_create_schema)

        return route

    def _get(self) -> Callable:
        async def route(pk: int, db: Session = Depends(get_db)):
            try:
                return self.model.manager(db).get(pk=pk)
            except ObjectDoesNotExists:
                raise HTTPException(status_code=400, detail=f"{self.model.__name__} does not exists")

        return route

    def _update(self) -> Callable:
        async def route(pk, update_schema: self.update_schema, db: Session = Depends(get_db)):
            return self.model.manager(db).update(pk, update_schema)

        return route

    def _delete(self) -> Callable:
        async def route(pk, db: Session = Depends(get_db)):
            return self.model.manager(db).delete(pk=pk)

        return route

    @staticmethod
    def get_routes() -> list:
        return [
            'get_all',
            'create',
            'get',
            'update',
            'delete'
        ]
