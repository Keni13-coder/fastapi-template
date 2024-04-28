from app.schemas.base_error import ExampleErrorResponse, Error
from app.exceptions.not_found import NotFoundEntity


class V1ResponseError(ExampleErrorResponse[Error]): ...


not_found_400 = V1ResponseError(
    status_code=NotFoundEntity.status_code,
    description="Ошибка нахождения сущности в коде, возникает из-за передачи с не валидными данными",
    content_example={"loc": ("example_loc",), "msg": NotFoundEntity.msg, "input": {}},
)
