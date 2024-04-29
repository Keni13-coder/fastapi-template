from datetime import timedelta
import pytest
import uuid

from app.core.config import settings
from app.utils.utc_now import datetime_utc


@pytest.fixture(scope="module")
def create_jwt_access(rewrite_lifetime):
    now = datetime_utc()
    return dict(
        device_id=uuid.uuid4(),
        user_uid=uuid.uuid4(),
        iat=datetime_utc(),
        exp=now + timedelta(minutes=settings.expired_access),
    )


@pytest.fixture(scope="module")
def create_jwt_refresh(rewrite_lifetime):
    now = datetime_utc()
    return dict(
        jti=uuid.uuid4(),
        user_uid=uuid.uuid4(),
        iat=datetime_utc(),
        exp=now + timedelta(minutes=settings.expired_access),
    )
