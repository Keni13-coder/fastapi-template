import abc
from typing import Generic, Type, TypeVar, Union

import pydantic
from sqlalchemy.inspection import inspect

from app.db.base import Base
from app.schemas.token import TokenSchema
from app.schemas.user import ResponseUserSchema


SerializeSchema = TypeVar("SerializeSchema", bound=Union[pydantic.BaseModel, dict])


class ABCEntitySerializer(abc.ABC, Generic[SerializeSchema]):

    def __init__(
        self,
        serialize_schema: Type[SerializeSchema],
    ) -> None:
        self._serialize_schema = serialize_schema

    @abc.abstractmethod
    def to_dict(self, data: Union[Base, dict]) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    def to_schema_or_dict(self, data: Union[Base, dict]) -> SerializeSchema:
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def to_own_scheme(
        data: Union[Base, dict], schema: pydantic.BaseModel
    ) -> pydantic.BaseModel:
        raise NotImplementedError

    @property
    def serialize_schema(self):
        return self._serialize_schema


class BaseSerializer(ABCEntitySerializer[SerializeSchema]):

    def to_dict(self, data: Base) -> dict:
        if issubclass(self._serialize_schema, dict):
            return {
                c.key: getattr(data, c.key) for c in inspect(data).mapper.column_attrs
            }
        return {}

    def to_schema_or_dict(self, data: Union[Base, dict]) -> SerializeSchema:
        if issubclass(self._serialize_schema, pydantic.BaseModel):
            return self._serialize_schema.model_validate(data, from_attributes=True)
        else:
            return data if isinstance(data, dict) else self.to_dict(data)

    @staticmethod
    def to_own_scheme(
        data: Union[Base, dict], schema: pydantic.BaseModel
    ) -> pydantic.BaseModel:
        return schema.model_validate(data, from_attributes=True)


class TokenEntitySerializer(BaseSerializer[TokenSchema]): ...


class UserEntitySerializer(BaseSerializer[ResponseUserSchema]): ...
