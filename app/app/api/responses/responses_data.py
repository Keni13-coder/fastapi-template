import enum
from .response_generator import generator_response
from app.exceptions.not_found import NotFoundEntity
from app.exceptions.error_server_500 import ServerError
from app.exceptions.jwt_error import (
    InvalidTokenException,
    TokenExpiredException,
    TokenNotAuthenticatedException,
)
from app.exceptions.user_error import RegisterException, AUTHException


class ResponsesError(enum.Enum):
    not_found_400 = generator_response.gener_error_responses(
        class_error=NotFoundEntity,
        description="Ошибка нахождения сущности в коде, возникает из-за передачи с не валидными данными",
    )
    server_500 = generator_response.gener_error_responses(
        class_error=ServerError,
        description="Неизвестная ошибка вызванная на стороне сервера",
        loc=("dispatch",),
    )
    register_400 = generator_response.gener_error_responses(
        class_error=RegisterException,
        description="Ошибка вызванная проверкой существования пользователя, из-за чего регистарция не возможна",
        loc=("register_user",),
    )
    auth_403 = generator_response.gener_error_responses(
        class_error=AUTHException,
        description="Ошибка вызванная при прохождении аунтефикации пользователя, говорящая о не валидности данных",
        loc=("login_user",),
    )
    invalid_token_403 = generator_response.gener_error_responses(
        class_error=InvalidTokenException,
        description="Ошибка вызванная несоответсвий данных при декодировании",
        loc=("decode_token_in_option",),
    )
    expired_token_403 = generator_response.gener_error_responses(
        class_error=TokenExpiredException,
        description="Ошибка вызванная передачей не истёкшиго токена, когда требуеться истекший",
        loc=("decode_token",),
    )
    not_auth_401 = generator_response.gener_error_responses(
        class_error=TokenNotAuthenticatedException,
        description="Ошибка вызванная при неправильной передачи схемы аунтефикации",
    )
