from dataclasses import dataclass

from pydantic import BaseModel
from fastapi import Form


class LoginUser(BaseModel):
    login: str
    password: str


@dataclass
class FormAuth:
    login: str = Form()
    password: str = Form(
        pattern="[A-Za-z0-9@#$%^&+=]{4,}",
        min_length=4,
        max_length=100,
    )

    def __post_init__(self):
        return LoginUser(login=self.login, password=self.password).model_dump_json()
