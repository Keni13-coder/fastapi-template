from typing import Optional, TypedDict
from fastapi import HTTPException
from app.schemas.base_error import Error


class ErrorRepresentation(TypedDict):
    loc: tuple
    msg: str
    input: Optional[dict] = {}


class StatusCodeDescr:
    def __get__(self, instance, owner):
        return str(owner._status_code)


class MessageDescr:
    def __get__(self, instance, owner):
        return owner._msg


class BaseErrorHTTPException(HTTPException):
    _status_code = None
    _msg = None

    status_code = StatusCodeDescr()
    msg = MessageDescr()

    def __init__(
        self, *loc, input: Optional[dict] = {}, headers: Optional[dict] = {}
    ) -> None:

        detail = self.conventional_error_message(
            error={"loc": tuple(loc), "msg": self._msg, "input": input}
        )
        super().__init__(status_code=self._status_code, detail=detail, headers=headers)

    def conventional_error_message(self, error: ErrorRepresentation):
        er = Error.model_validate(error)
        message_data = {
            "detail": [
                {
                    "loc": f"({','.join(er.loc)})",
                    "msg": er.msg,
                    "input": er.input if er.input else {},
                },
            ]
        }
        return message_data

    # def __getattr__(self, item):
    #     raise ValueError(f'There is no attribute named {item}')
