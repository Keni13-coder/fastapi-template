from typing import AsyncGenerator
import pytest

from app.schemas.user import CreateUser
from app.uow.context.uow_context import FakeUOW, FakeUOWContext
from app.services.user import ABCUserService, UserService
from app.services.jwt_service import ABCJWT, JWTService
from app.services.token import ABCTokenService, TokenService
from app.core.config import settings

# region ContextUOW


@pytest.fixture(scope="session")
async def get_fakeUOW() -> FakeUOWContext:
    return FakeUOW


# endregion


# region Service
@pytest.fixture(scope="session")
async def user_service() -> ABCUserService:
    return UserService


@pytest.fixture(scope="session")
async def jwt_service() -> ABCJWT:
    return JWTService(algorithm=settings.algorithm, secret_key=settings.secret_key)


@pytest.fixture(scope="session")
async def token_service() -> ABCTokenService:
    return TokenService(jwt_service=JWTService)


# endregion


# utils fixture
@pytest.fixture(scope="session")
async def get_user_fake(create_data_user: CreateUser):
    async with FakeUOW as uow:
        data = create_data_user
        data = data.model_dump(exclude={"confirm_password"})
        data["id"] = "1"
        user = await uow.user.create(obj_in=data)
        assert user

        return user
