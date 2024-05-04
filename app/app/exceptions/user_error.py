from fastapi import status

from .base import BaseErrorHTTPException


class AUTHException(BaseErrorHTTPException):
    _status_code = status.HTTP_403_FORBIDDEN
    _msg = "Error, the transmitted data is not valid"


class RegisterException(BaseErrorHTTPException):
    _status_code = status.HTTP_400_BAD_REQUEST
    _msg = "Error, this user is already registered"
