from datetime import timedelta
import uuid
import pytest

from app.uow.typing.fake_type_protocol import FakeUOWContextProtocol
from app.exceptions.jwt_error import TokenExpiredException
from app.services.user import ABCUserService
from app.services.token import ABCTokenService
from app.services.jwt_service import ABCJWT
from tests.unit.utils import assertional_session_aexit
from app.utils.utc_now import datetime_utc


class TestUserService:

    async def test_get_user(
        self,
        get_fakeUOW: FakeUOWContextProtocol,
        user_service: ABCUserService,
        get_user_fake,
    ):
        user = await user_service.get_user(get_user_fake["id"], get_fakeUOW)
        assert user

    async def test_list_users(self, get_fakeUOW, user_service: ABCUserService):
        users = await user_service.list_users(get_fakeUOW)
        assert users
        assert len(users) == 1


@pytest.fixture(scope="class")
def data_access():
    _access_token = ""

    def token(access_token=""):
        global _access_token
        if access_token:
            _access_token = access_token
            return access_token
        else:
            return _access_token

    yield token

    _access_token = ""


@pytest.fixture(scope="class")
def data_refresh():
    _refresh_token = ""

    def token(refresh_token=""):
        global _refresh_token
        if refresh_token:
            _refresh_token = refresh_token
            return refresh_token
        else:
            return _refresh_token

    yield token

    _refresh_token = ""


class TestJWTService:
    async def test_create_accsess_jwt(
        self, jwt_service: ABCJWT, create_jwt_access: dict, data_access
    ):
        access = await jwt_service.create_accsess_jwt(**create_jwt_access)
        assert access
        assert data_access(access)

    async def test_create_refresh_jwt(
        self, jwt_service: ABCJWT, create_jwt_refresh: dict, data_refresh
    ):
        refresh = await jwt_service.create_refresh_jwt(**create_jwt_refresh)
        assert refresh
        assert data_refresh(refresh)

    async def test_decode_access_token(self, jwt_service: ABCJWT, data_access):
        access_payload = await jwt_service.decode_token(data_access())
        assert isinstance(access_payload, dict)
        assert access_payload.get("device_id")

    async def test_decode_refresh_token(self, jwt_service: ABCJWT, data_refresh):
        refresh_payload = await jwt_service.decode_token(data_refresh())
        assert isinstance(refresh_payload, dict)
        assert refresh_payload.get("jti")

    async def test_decode_expired(self, jwt_service: ABCJWT, data_access):
        """Должен вызвать ошибку, так как мы только создали токен и он не истек"""
        with pytest.raises(TokenExpiredException):
            await jwt_service.decode_token(data_access(), expired=True)

    async def test_create_access_refresh_jwt(self, jwt_service: ABCJWT):
        """Проверка создание двух токенов, с возможностью передачи expire_refresh, для обновление refresh_token со старым exp параметром"""
        now = datetime_utc()
        device_id = uuid.uuid4()
        jti = uuid.uuid4()
        user_uid = uuid.uuid4()
        expire_refresh = int((now + timedelta(minutes=1)).timestamp())

        result_without_expire = await jwt_service.create_access_refresh_jwt(
            device_id=device_id, jti=jti, user_uid=user_uid, now=now
        )
        assert result_without_expire

        result_with_expire = await jwt_service.create_access_refresh_jwt(
            device_id=device_id,
            jti=jti,
            user_uid=user_uid,
            now=now,
            expire_refresh=expire_refresh,
        )

        assert result_with_expire

        decode_refresh_without_expire = await jwt_service.decode_token(
            result_without_expire.refresh_token
        )
        decode_refresh_with_expire = await jwt_service.decode_token(
            result_with_expire.refresh_token
        )

        assert decode_refresh_without_expire["exp"] != decode_refresh_with_expire["exp"]


class TestTokenService:
    async def test_create_pair_tokens(
        self, get_fakeUOW: FakeUOWContextProtocol, token_service: ABCTokenService
    ):
        user_id = uuid.uuid4()
        tokens = await token_service.create_pair_tokens(
            user_uid=user_id, uow_context=get_fakeUOW
        )
        assert tokens
        assert get_fakeUOW.session.is_commit
        await assertional_session_aexit(get_fakeUOW)
