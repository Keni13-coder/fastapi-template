from typing import AsyncGenerator
import uuid
import pytest

from app.schemas.user import CreateUser, ResponseUserSchema
from app.uow.context.uow_context import FakeUOW, FakeUOWContext
from app.services.user import ABCUserService, UserService
from app.services.jwt_service import ABCJWT, JWTService
from app.services.token import ABCTokenService, TokenService, TokenSchema
from app.services.serialize_model import TokenEntitySerializer, UserEntitySerializer


from app.core.config import settings


# region ContextUOW
@pytest.fixture(scope="class")
def get_fakeUOW() -> FakeUOWContext:
    return FakeUOW


# endregion


# region Service
@pytest.fixture(scope="package")
def user_service() -> ABCUserService:
    return UserService


@pytest.fixture(scope="module")
def jwt_service() -> ABCJWT:
    return JWTService(algorithm=settings.algorithm, secret_key=settings.secret_key)


@pytest.fixture(scope="class")
def token_service() -> ABCTokenService:
    return TokenService(
        jwt_service=JWTService,
        serializer=TokenEntitySerializer(serialize_schema=TokenSchema),
    )


# endregion


# utils fixture region
@pytest.fixture
async def get_user_fake(create_data_user: CreateUser):
    serializer = UserEntitySerializer(serialize_schema=ResponseUserSchema)
    async with FakeUOW as uow:
        data = create_data_user
        data = data.model_dump()
        user = await uow.user.create(obj_in=data)
        assert user

        return serializer.to_schema_or_dict(user)


# endregion


# start region
@pytest.fixture(scope="module")
def high_lifetime():
    settings.expired_access = 20


@pytest.fixture
def last_time_refresh():
    settings.expired_access = 20
    yield
    settings.expired_access = 0


@pytest.fixture(scope="class")
def low_lifetime():
    settings.expired_access = 0
    settings.expired_refresh = 10
