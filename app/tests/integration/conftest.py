import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user import RepositoryUser
from app.uow.context.uow_context import UOWV1
from app.services.user import ABCUserService, UserService
from app.services.subdomain.serialize_service import UserEntitySerializer
from app.schemas.user import ResponseUserSchema
from app.services.subdomain.hasher_service import Hasher


@pytest.fixture
def repository_user(get_session):
    return RepositoryUser(session=get_session)

@pytest.fixture(scope="class")
def user_service(token_service) -> ABCUserService:
    return UserService(
        token_service=token_service,
        serializer=UserEntitySerializer(ResponseUserSchema),
        hasher_class=Hasher()
        )




@pytest.fixture(scope="class")
def get_uow():
    return UOWV1


@pytest.fixture(scope="class")
def data_user(request):
    result = request.getfixturevalue(request.param)
    return result
