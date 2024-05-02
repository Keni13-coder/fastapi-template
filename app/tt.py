from datetime import datetime, timedelta, timezone
from typing import Literal, Union
from pydantic import BaseModel, field_validator


class ResponseToken(BaseModel):
    refresh_token: str
    access_token: str
    expire_refresh: Union[int, datetime]
    token_type: Literal["bearer"] = "bearer"

    @field_validator("expire_refresh")
    @classmethod
    def exp_to_int(cls, v):
        if isinstance(v, int):
            return v
        return int(v.timestamp())


test = ResponseToken(
    refresh_token="assd",
    access_token="asd",
    expire_refresh=datetime.now(timezone.utc) + timedelta(minutes=1),
)
