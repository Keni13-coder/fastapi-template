from typing import Optional
from uuid import UUID
from datetime import datetime

from fastapi import HTTPException, status
from pydantic import BaseModel, Field, validator, model_validator

from app.utils.const import UserRole


class BaseUser(BaseModel):
    login: str = Field(title="Логин")
    created_at: datetime = Field(title="Создан", default_factory=datetime.now)
    updated_at: datetime = Field(title="Обновлен", default_factory=datetime.now)


class ResponseUserSchema(BaseUser):
    id: UUID | None = Field(title="ID", default=None)
    is_active: bool = Field(title="Активность", default=True)
    role: UserRole = Field(title="Роль пользователя", default=UserRole.user)


class UserPassword(BaseModel):
    password: str = Field(
        ...,
        title="password",
        pattern="[A-Za-z0-9@#$%^&+=]{4,}",
        min_length=4,
        max_length=100,
        alias="hashed_password",
    )


class CreateUser(BaseUser, UserPassword): ...


class UpdateLogin(BaseModel):
    login: str = Field(title="Логин")
    updated_at: datetime = Field(title="Обновлен", default_factory=datetime.now)


class СhangePassword(UserPassword): ...


class UpdateUser(BaseModel):
    update_login: Optional[UpdateLogin] = None
    update_password: Optional[СhangePassword] = None

    @model_validator(mode="after")
    def valid_request_data(self):
        if not (self.update_login or self.update_password):
            er = {
                "loc": ("update_login", "update_password"),
                "msg": "Value error, 'At least 1 field must be filled in' is not a valid HTTPStatus",
                "input": f"{self.update_login=}, {self.update_password=}",
            }
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=er)
        return self
