from typing import List, Optional, Union, Generic, TypeVar

from fastapi import Query
from pydantic import BaseModel, Field, model_serializer
from app.core.config import settings


ResponseModel = TypeVar("ResponseModel", bound=BaseModel)


class Params(BaseModel):
    offset: int = Query(
        default=0,
        gt=0,
        description="Указывает количество строк, которые необходимо пропустить перед началом запроса",
    )
    limit: int = Query(
        default=1000, gt=0, lt=101, description="Ограничение количества выводимых строк"
    )


class PathInfo(BaseModel):
    is_cache: bool


class ResponseDefault(BaseModel, Generic[ResponseModel]):
    detail: List[ResponseModel]
    info_api: Optional[dict[str, PathInfo]] = Field(
        default={f"method{settings.api_v1_str}/*": PathInfo(is_cache=True)},
        description="Описывает конечные точки группы для взаимодействия",
    )


class ResponseMessage(BaseModel):
    message: str


class ResponseWithParams(ResponseDefault):
    params: Params = Field(
        ..., description="Значения пропуска и считывания строк данных"
    )
