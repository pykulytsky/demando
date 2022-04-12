from typing import Optional, Type

from pydantic import BaseConfig, BaseModel, create_model
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.properties import ColumnProperty

from base.exceptions import NotValidModel


class OrmConfig(BaseConfig):
    orm_mode = True


class OrmModel(BaseModel):
    @classmethod
    def from_db_model(model, config: Type = OrmConfig):
        try:
            inspection = inspect(model)

            fields = {}
            for attr in inspection.attrs:
                if isinstance(attr, ColumnProperty):
                    if attr.columns:
                        name = attr.key
                        column = attr.columns[0]
                        python_type: Optional[type] = None
                        if hasattr(column.type, "impl"):
                            if hasattr(column.type.impl, "python_type"):
                                python_type = column.type.impl.python_type
                        elif hasattr(column.type, "python_type"):
                            python_type = column.type.python_type

                        default = None
                        if column.default is None and not column.nullable:
                            default = ...
                        fields[name] = (python_type, default)
            pydantic_model = create_model(
                model.__name__, __config__=config, **fields  # type: ignore
            )
            return pydantic_model
        except TypeError as e:
            raise NotValidModel(e)
