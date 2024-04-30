import asyncio
import pytest
from app.exceptions.jwt_error import InvalidTokenException
from app.exceptions.not_found import NotFoundEntity
from app.repositories.user import RepositoryUser
from app.services.token import ABCTokenService
from app.uow.typing.type_protocol import UOWContextProtocol
from app.schemas.user import ResponseUserSchema


@pytest.fixture
async def current_user(get_session, create_data_user) -> ResponseUserSchema:
    user_repo = RepositoryUser(session=get_session)
    user = await user_repo.create(obj_in=create_data_user)
    await get_session.commit()
    return user


# Возможно стоит перенести на unit тесты
# Возможно посмотреть Userservice, переносить или возможно на unit
@pytest.mark.usefixtures("prepare_database")
class TestTokenService:
    """Тестерум создание и обновление пар токенов, для этого утсановите
    expired_access=0 в env configuration
    """

    tokens = {}

    async def test_create_pair_tokens(
        self,
        get_uow: UOWContextProtocol,
        token_service: ABCTokenService,
        current_user: ResponseUserSchema,
    ):
        tokens = await token_service.create_pair_tokens(
            user_uid=current_user.id, uow_context=get_uow
        )
        assert tokens
        async with get_uow as uow:
            token = await uow.token.get(user_uid=current_user.id)
            assert token

        self.tokens["access_token"] = tokens.access_token
        self.tokens["refresh_token"] = tokens.refresh_token

    async def test_refresh_pair_tokens(
        self, get_uow: UOWContextProtocol, token_service: ABCTokenService
    ):
        """Проверка старого токена и нового, также проверить логики удаления у одного и у двух пользователей"""

        assert self.tokens
        await asyncio.sleep(3)
        token_data = await token_service.refresh_pair_tokens(
            access_token_encode=self.tokens["access_token"],
            refresh_token_encode=self.tokens["refresh_token"],
            uow_context=get_uow,
        )

        async with get_uow as uow:
            list_token = await uow.token.list()

            assert list_token and len(list_token) == 1

        assert token_data
        self.tokens["refresh_token"] = token_data.refresh_token

    async def test_raise_refresh_pair_tokens(
        self, get_uow: UOWContextProtocol, token_service: ABCTokenService
    ):
        assert self.tokens

        with pytest.raises(InvalidTokenException):
            await token_service.refresh_pair_tokens(
                access_token_encode=self.tokens["access_token"],
                refresh_token_encode=self.tokens["refresh_token"],
                uow_context=get_uow,
            )
        async with get_uow as uow:
            assert not await uow.token.list()

        with pytest.raises(NotFoundEntity):
            await token_service.refresh_pair_tokens(
                access_token_encode=self.tokens["access_token"],
                refresh_token_encode=self.tokens["refresh_token"],
                uow_context=get_uow,
            )
