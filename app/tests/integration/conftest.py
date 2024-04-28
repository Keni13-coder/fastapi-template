import pytest
from _pytest.fixtures import SubRequest

from app.repositories.user import RepositoryUser, CreateUser, UpdateUser
from tests.integration.utils import TestUserIntegration


# user region
@pytest.fixture(scope="module")
def start_user(
    get_session, create_data_user: CreateUser, update_data_user_login: UpdateUser
):
    user_integration = TestUserIntegration(
        repository=RepositoryUser(session=get_session),
        get_session=get_session,
        CreateSchema=create_data_user.model_dump(exclude={"confirm_password"}),
        UpdateSchema=update_data_user_login,
    )

    return user_integration


# endregion


# start region
@pytest.fixture(scope="module")
def starter_repository(request: SubRequest):
    result = request.getfixturevalue(request.param)
    return result


@pytest.fixture(scope="session", autouse=True)
async def setup_dependencies_base(prepare_database):
    return


# endregion
