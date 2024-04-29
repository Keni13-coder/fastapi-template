import pytest
import uuid
from app.schemas.token import RefreshToken, UpdateTokens
from app.utils.utc_now import datetime_utc


@pytest.fixture(scope="module")
def create_data_token():
    return RefreshToken(
        jti=uuid.uuid4(),
        user_uid=uuid.uuid4(),
        device_id=uuid.uuid4(),
        access_iat=datetime_utc(),
    ).model_dump()


@pytest.fixture(scope="module")
def update_data_token():
    return UpdateTokens(jti=uuid.uuid4(), access_iat=datetime_utc()).model_dump()
