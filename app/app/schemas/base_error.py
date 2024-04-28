from typing import Optional, Generic, TypeVar

from pydantic import BaseModel, model_serializer


class Error(BaseModel):
    loc: tuple
    msg: str
    input: Optional[dict] = {}


class ResponseError(BaseModel):
    detail: Error


TypeResponseError = TypeVar("TypeResponseError", bound=Error)


class ExampleErrorResponse(BaseModel, Generic[TypeResponseError]):
    status_code: str
    description: str
    content_example: TypeResponseError
    model: TypeResponseError = Error

    @model_serializer()
    def conversion_to_error_response(self):
        self.model.model_validate(self.content_example)
        response = {
            self.status_code: {
                "model": self.model,
                **self.generate_exepemple_response(
                    self.description, self.content_example
                ),
            }
        }
        return response

    def generate_exepemple_response(
        self, description: str, content_example: dict[str, str]
    ) -> dict:
        response = {
            "description": description,
            "content": {"application/json": {"example": {"detail": [content_example]}}},
        }
        return response
