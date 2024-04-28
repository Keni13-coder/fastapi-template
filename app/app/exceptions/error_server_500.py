from fastapi import status

from .base import BaseErrorHTTPException


class ServerError(BaseErrorHTTPException):
    _status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    _msg = "Error, an unknown error occurred on the server side"
