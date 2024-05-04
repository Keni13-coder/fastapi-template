from typing import Type
from pydantic import BaseModel

from .response_schemas import V1ResponseError
from app.exceptions.base import BaseErrorHTTPException


class GeneratorResponses:

    def __init__(self, error_schema: Type[V1ResponseError] = V1ResponseError) -> None:
        self._error_schema = error_schema

    def gener_error_responses(
        self,
        class_error: Type[BaseErrorHTTPException],
        description: str,
        loc: tuple = tuple(),
    ):
        return self._error_schema(
            status_code=class_error.status_code,
            description=description,
            content_example={
                "loc": ("example_loc",) if not loc else loc,
                "msg": class_error.msg,
                "input": {},
            },
        )

    def create_responses_for_point(self, *responses: BaseModel) -> dict:
        create_data = dict()
        for response in responses:
            create_data.update(response.model_dump())
        return create_data


generator_response = GeneratorResponses(error_schema=V1ResponseError)
