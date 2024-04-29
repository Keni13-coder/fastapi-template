import pytest

from app.repositories.user import RepositoryUser
from app.services.jwt_service import JWTService
from app.services.token import ABCTokenService, TokenService
from app.uow.context.uow_context import UOWV1



@pytest.fixture
def repository_user(
    get_session
):
    return RepositoryUser(session=get_session)

@pytest.fixture(scope="class")
def token_service() -> ABCTokenService:
    return TokenService(jwt_service=JWTService)


@pytest.fixture(scope="class")
def get_uow():
    return UOWV1


@pytest.fixture(scope='class')
def data_user(request):
    result = request.getfixturevalue(request.param)
    return result