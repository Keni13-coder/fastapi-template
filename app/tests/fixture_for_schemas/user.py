import pytest
from app.schemas.user import CreateUser, UpdateUser, UpdateLogin, СhangePassword


@pytest.fixture(scope="session")
async def create_data_user() -> CreateUser:
    return CreateUser(
        hashed_password="1313",
        confirm_password="1313",
        login="vladislavic",
    )


@pytest.fixture(scope="session")
async def update_data_user_login() -> UpdateLogin:
    return UpdateUser(update_login=dict(login="newlogin")).update_login


@pytest.fixture(scope="session")
async def update_data_user_password() -> СhangePassword:
    return UpdateUser(
        update_password=dict(password="1414", confirm_password="1414")
    ).update_password
