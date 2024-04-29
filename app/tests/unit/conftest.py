from typing import AsyncGenerator
import pytest

from app.schemas.user import CreateUser
from app.uow.context.uow_context import FakeUOW, FakeUOWContext
from app.services.user import ABCUserService, UserService
from app.services.jwt_service import ABCJWT, JWTService

from app.core.config import settings


# region ContextUOW
@pytest.fixture(scope='package')
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

# endregion


# utils fixture region
@pytest.fixture
async def get_user_fake(create_data_user: CreateUser):
    async with FakeUOW as uow:
        data = create_data_user
        data = data.model_dump()
        data["id"] = "1"
        user = await uow.user.create(obj_in=data)
        assert user

        return user
# endregion

# start region
@pytest.fixture(scope='module')
def rewrite_lifetime():
    settings.expired_access = 20
