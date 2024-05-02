from datetime import timedelta
import uuid
import pytest
import asyncio

from app.exceptions.jwt_error import TokenExpiredException, InvalidTokenException
from app.exceptions.not_found import NotFoundEntity
from app.services.user import ABCUserService, ResponseUserSchema
from app.services.token import ABCTokenService
from app.services.jwt_service import ABCJWT
from app.uow.typing.fake_type_protocol import FakeUOWContextProtocol
from app.utils.utc_now import datetime_utc


class TestUserService:

    async def test_get_user(
        self,
        get_fakeUOW: FakeUOWContextProtocol,
        user_service: ABCUserService,
        get_user_fake: ResponseUserSchema,
    ):
        user = await user_service.get_user(get_user_fake.id, get_fakeUOW)
        assert user

    async def test_list_users(self, get_fakeUOW, user_service: ABCUserService):
        users = await user_service.list_users(get_fakeUOW)
        assert users
        assert len(users) == 1


@pytest.mark.usefixtures("high_lifetime")
class TestJWTService:
    data_access = {"access_token": ""}
    data_refresh = {"refresh_token": ""}

    async def test_create_accsess_jwt(
        self, jwt_service: ABCJWT, create_jwt_access: dict
    ):
        access = await jwt_service.create_accsess_jwt(**create_jwt_access)
        assert access
        self.data_access["access_token"] = access

    async def test_create_refresh_jwt(
        self, jwt_service: ABCJWT, create_jwt_refresh: dict
    ):
        refresh = await jwt_service.create_refresh_jwt(**create_jwt_refresh)
        assert refresh
        self.data_refresh["refresh_token"] = refresh

    async def test_decode_access_token(self, jwt_service: ABCJWT):
        assert self.data_access["access_token"]
        access_payload = await jwt_service.decode_token(
            self.data_access["access_token"]
        )
        assert isinstance(access_payload, dict)
        assert access_payload.get("device_id")

    async def test_decode_refresh_token(self, jwt_service: ABCJWT):
        refresh_payload = await jwt_service.decode_token(
            self.data_refresh["refresh_token"]
        )
        assert isinstance(refresh_payload, dict)
        assert refresh_payload.get("jti")

    async def test_decode_expired(self, jwt_service: ABCJWT):
        """Должен вызвать ошибку, так как мы только создали токен и он не истек"""
        with pytest.raises(TokenExpiredException):
            await jwt_service.decode_token(
                self.data_access["access_token"], expired=True
            )

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


@pytest.mark.usefixtures("low_lifetime")
class TestTokenService:
    """Тестерум создание и обновление пар токенов, для этого утсановите
    expired_access=0 в env configuration
    """

    tokens = {}

    async def test_create_pair_tokens(
        self,
        get_fakeUOW: FakeUOWContextProtocol,
        token_service: ABCTokenService,
        get_user_fake: ResponseUserSchema,
    ):
        tokens = await token_service.create_pair_tokens(
            user_uid=get_user_fake.id, uow_context=get_fakeUOW
        )
        assert tokens
        async with get_fakeUOW as uow:
            token = await uow.token.get(user_uid=get_user_fake.id)
            assert token
        self.tokens["access_token"] = tokens.access_token
        self.tokens["refresh_token"] = tokens.refresh_token

    async def test_refresh_pair_tokens(
        self, get_fakeUOW: FakeUOWContextProtocol, token_service: ABCTokenService
    ):
        """Проверка старого токена и нового, также проверить логики удаления у одного и у двух пользователей"""

        assert self.tokens
        await asyncio.sleep(1)  # для создание токенов с разрывом по времени
        token_data = await token_service.refresh_pair_tokens(
            access_token_encode=self.tokens["access_token"],
            refresh_token_encode=self.tokens["refresh_token"],
            uow_context=get_fakeUOW,
        )
        assert token_data

        async with get_fakeUOW as uow:
            list_token = await uow.token.list()

            assert list_token and len(list_token) == 1

        self.tokens["refresh_token"] = token_data.refresh_token
        self.tokens["access_token"] = token_data.access_token

    @pytest.mark.usefixtures("last_time_refresh")
    async def test_last_refresh_pair_tokens(
        self, get_fakeUOW: FakeUOWContextProtocol, token_service: ABCTokenService
    ):
        assert self.tokens

        token_data = await token_service.refresh_pair_tokens(
            access_token_encode=self.tokens["access_token"],
            refresh_token_encode=self.tokens["refresh_token"],
            uow_context=get_fakeUOW,
        )
        assert token_data

        async with get_fakeUOW as uow:
            list_token = await uow.token.list()

            assert not list_token

        self.tokens["refresh_token"] = token_data.refresh_token

    async def test_raise_NotFoundEntity(
        self, get_fakeUOW: FakeUOWContextProtocol, token_service: ABCTokenService
    ):

        with pytest.raises(NotFoundEntity):
            await token_service.refresh_pair_tokens(
                access_token_encode=self.tokens["access_token"],
                refresh_token_encode=self.tokens["refresh_token"],
                uow_context=get_fakeUOW,
            )
    async def test_raise_InvalidTokenException(
        self,
        get_fakeUOW: FakeUOWContextProtocol,
        token_service: ABCTokenService,
        get_user_fake: ResponseUserSchema,
    ):

        pair_token = await token_service.create_pair_tokens(
            user_uid=get_user_fake.id, uow_context=get_fakeUOW
        )
        async with get_fakeUOW as uow:
            list_token = await uow.token.list()
            assert list_token

        with pytest.raises(InvalidTokenException):
            await token_service.refresh_pair_tokens(
                access_token_encode=self.tokens["access_token"],
                refresh_token_encode=pair_token.refresh_token,
                uow_context=get_fakeUOW,
            )
        async with get_fakeUOW as uow:
            assert not await uow.token.list()

    @pytest.mark.usefixtures("high_lifetime")
    async def test_delete_token(
        self,
        get_fakeUOW: FakeUOWContextProtocol,
        token_service: ABCTokenService,
        get_user_fake: ResponseUserSchema,
    ):
        pair_token = await token_service.create_pair_tokens(
            user_uid=get_user_fake.id, uow_context=get_fakeUOW
        )
        async with get_fakeUOW as uow:
            list_token = await uow.token.list()
            assert list_token

        result = await token_service.delete_token(
            access_token_encode=pair_token.access_token, uow_context=get_fakeUOW
        )
        assert result is None
