from fastapi import status

from .base import BaseErrorHTTPException


class NotFoundEntity(BaseErrorHTTPException):
    _status_code = status.HTTP_400_BAD_REQUEST
    _msg = "Error, the transmitted values have not been confirmed"
