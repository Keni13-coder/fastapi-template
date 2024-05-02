from datetime import datetime
from typing import Literal, Optional, Union
from uuid import UUID
from pydantic import UUID4, BaseModel, Field, field_validator, model_validator


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

    @field_validator("expire_refresh")
    @classmethod
    def exp_to_int(cls, v):
        if isinstance(v, int):
            return v
        return int(v.timestamp())


class Payload(BaseModel):
    exp: int
    nbf: int


class PayloadToken(Payload):
    user_uid: Union[UUID4, str] = Field(..., alias="sub")
    device_id: Union[UUID4, str]

    @model_validator(mode="after")
    def str_in_uuid(self):
        if isinstance(self.user_uid, str):
            self.user_uid = UUID(self.user_uid)
        if isinstance(self.device_id, str):
            self.device_id = UUID(self.device_id)

        return self

    class Config:
        populate_by_name = True
