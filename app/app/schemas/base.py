from typing import List, Generic, TypeVar, Union

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, model_validator
from app.utils.hateoas import hateoas_gener


ResponseModel = TypeVar("ResponseModel", bound=Union[BaseModel, dict])
APIRequest = TypeVar('APIRequest')


class Params(BaseModel):
    offset: int = Query(
        default=0,
        ge=0,
        description="Указывает количество строк, которые необходимо пропустить перед началом запроса",
    )
    limit: int = Query(
        default=1000, gt=0, lt=1001, description="Ограничение количества выводимых строк"
    )

class PathInfo(BaseModel):
    is_cache: bool  = Field(default=False, description='Указывает на кешируемый ли объект')
    request: APIRequest = Field(
        alias='info_api',
        json_schema_extra=
            {
                'title': 'info_api',
                'description': 'Показывает маршруты относящиеся к конечной точки',
                'examples': [['[Method/example_url/', '...']],
                'type': 'list'
            }
            
        )
    model_config = ConfigDict(populate_by_name=True)
          
    @model_validator(mode='after')
    def hateoas(self):
        self.request: tuple = hateoas_gener(self.request)
        return self
    
    
class ResponseDefault(PathInfo, Generic[ResponseModel]):
    detail: List[ResponseModel]
    

class ResponseMessage(BaseModel):
    message: str


class ResponseWithParams(ResponseDefault):
    params: Params = Field(
        ..., description="Значения пропуска и считывания строк данных"
    )
