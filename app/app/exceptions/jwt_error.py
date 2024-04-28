from typing import Optional
from fastapi import status

from .base import BaseErrorHTTPException


class InvalidTokenException(BaseErrorHTTPException):
    _status_code = status.HTTP_403_FORBIDDEN
    _msg = "Error, invalid token"


class TokenExpiredException(BaseErrorHTTPException):
    _status_code = status.HTTP_403_FORBIDDEN
    _msg = "Error, the token must be expired"


class TokenNotAuthenticatedException(BaseErrorHTTPException):
    _status_code = status.HTTP_401_UNAUTHORIZED
    _msg = "Error, Not authenticated"
