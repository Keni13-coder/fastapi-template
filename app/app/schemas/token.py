from datetime import datetime
from typing import Literal, Union
from pydantic import UUID4, BaseModel, field_validator


class RefreshToken(BaseModel):
    jti: UUID4
    user_uid: UUID4
    device_id: UUID4
    access_iat: datetime


class TokenSchema(RefreshToken):
    id: UUID4


class UpdateTokens(BaseModel):
    jti: UUID4
    access_iat: datetime


class TokenLoginResponse(BaseModel):
    access_token: str
    expire_refresh: Union[int, datetime]
    token_type: Literal["bearer"] = "bearer"

    @field_validator("expire_refresh")
    @classmethod
    def exp_to_int(cls, v):
        if isinstance(v, int):
            return v
        return int(v.timestamp())

class ResponseToken(TokenLoginResponse):
    refresh_token: str