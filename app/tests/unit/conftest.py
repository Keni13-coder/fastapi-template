import pytest

from app.schemas.user import CreateUser, ResponseUserSchema
from app.uow.context.uow_context import FakeUOW, FakeUOWContext
from app.services.subdomain.jwt_service import ABCJWT, JWTService
from app.services.subdomain.serialize_service import UserEntitySerializer
from app.utils.utc_now import datetime_utc


from app.core.config import settings


# region ContextUOW
@pytest.fixture(scope="class")
def get_fakeUOW() -> FakeUOWContext:
    return FakeUOW


# endregion


@pytest.fixture(scope="class")
def jwt_service() -> ABCJWT:
    return JWTService(algorithm=settings.algorithm, secret_key=settings.secret_key)


# utils fixture region
@pytest.fixture
async def get_user_fake(create_data_user: CreateUser):
    serializer = UserEntitySerializer(serialize_schema=ResponseUserSchema)
    async with FakeUOW as uow:
        data = create_data_user
        data = data.model_dump()
        now = datetime_utc()
        data.update(dict(created_at=now, updated_at=now))
        user = await uow.user.create(obj_in=data)
        assert user

        return serializer.to_schema_or_dict(user)


# endregion


