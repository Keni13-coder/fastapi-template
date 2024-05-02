import pytest
from app.schemas.user import CreateUser, UpdateLogin, СhangePassword
from tests.unit.utils import assertional_session_aexit
from tests.unit.conftest import FakeUOWContext


class TestContextUser:

    user_data = {}
    async def test_create_user(
        self, get_fakeUOW: FakeUOWContext, create_data_user: CreateUser
    ):
        async with get_fakeUOW as uow:

            data = create_data_user.model_dump()
            user = await uow.user.create(obj_in=data)
            await uow.commit()

            assert get_fakeUOW.session.is_commit
            assert user
            assert len(uow.user._model) == 1
            self.user_data.update(user)

        assertional_session_aexit(get_fakeUOW)

    async def test_get_user(self, get_fakeUOW: FakeUOWContext):
        async with get_fakeUOW as uow:
            user = await uow.user.get(login="vladislavic")
            assert user

        assertional_session_aexit(get_fakeUOW)

    async def test_get_list_user(self, get_fakeUOW: FakeUOWContext):
        async with get_fakeUOW as uow:
            user = await uow.user.list()

            assert user
            assert len(user) == 1

        assertional_session_aexit(get_fakeUOW)

    async def test_update_user_login(
        self, get_fakeUOW: FakeUOWContext, update_data_user_login: UpdateLogin
    ):
        async with get_fakeUOW as uow:
            user = await uow.user.update(id=self.user_data['id'], obj_in=update_data_user_login)
            await uow.commit()

            assert get_fakeUOW.session.is_commit
            assert user
            assert user["login"] == "newlogin"

        assertional_session_aexit(get_fakeUOW)

    async def test_update_user_password(
        self, get_fakeUOW: FakeUOWContext, update_data_user_password: СhangePassword
    ):

        async with get_fakeUOW as uow:
            user = await uow.user.update(id=self.user_data['id'], obj_in=update_data_user_password)
            await uow.commit()

            assert get_fakeUOW.session.is_commit
            assert user
            assert user["password"] == "1414"

        assertional_session_aexit(get_fakeUOW)

    async def test_exists_true(self, get_fakeUOW: FakeUOWContext):
        async with get_fakeUOW as uow:
            result = await uow.user.exists(id=self.user_data['id'])
            assert result

        assertional_session_aexit(get_fakeUOW)

    async def test_delete_user(self, get_fakeUOW: FakeUOWContext):
        async with get_fakeUOW as uow:
            await uow.user.delete(id=self.user_data['id'])
            await uow.commit()

            assert get_fakeUOW.session.is_commit

            assert uow.user._model == []

        assertional_session_aexit(get_fakeUOW)

    async def test_exists_fasle(self, get_fakeUOW: FakeUOWContext):
        async with get_fakeUOW as uow:
            result = await uow.user.exists(id=self.user_data['id'])
            assert not result

        assertional_session_aexit(get_fakeUOW)


@pytest.mark.usefixtures('high_lifetime')
class TestContextToken:
    data_jti = {}

    async def test_create_token(
        self, get_fakeUOW: FakeUOWContext, create_data_token
    ):
        async with get_fakeUOW as uow:
            token = await uow.token.create(create_data_token)
            assert token
            assert len(uow.token._model) == 1

        assertional_session_aexit(get_fakeUOW)
        self.data_jti.update({'jti': create_data_token["jti"]}) 

    async def test_get_token(self, get_fakeUOW: FakeUOWContext):
        async with get_fakeUOW as uow:
            token = await uow.token.get(jti=self.data_jti['jti'])
            assert token

        assertional_session_aexit(get_fakeUOW)

    async def test_get_list_token(self, get_fakeUOW: FakeUOWContext):
        async with get_fakeUOW as uow:
            tokens = await uow.token.list()

            assert tokens
            assert len(tokens) == 1

        assertional_session_aexit(get_fakeUOW)

    async def test_update_token(
        self, get_fakeUOW: FakeUOWContext, update_data_token
    ):
        async with get_fakeUOW as uow:
            token = await uow.token.update(jti=self.data_jti['jti'], obj_in=update_data_token)
            assert token
            assert token["jti"] != self.data_jti['jti']
            self.data_jti.update({'jti': token["jti"]})
        assertional_session_aexit(get_fakeUOW)

    async def test_exists_true(self, get_fakeUOW: FakeUOWContext):

        async with get_fakeUOW as uow:
            assert await uow.token.exists(jti=self.data_jti['jti'])

        assertional_session_aexit(get_fakeUOW)

    async def test_delete_token(self, get_fakeUOW: FakeUOWContext):
        async with get_fakeUOW as uow:
            await uow.token.delete(jti=self.data_jti['jti'])
            assert uow.token._model == []

        assertional_session_aexit(get_fakeUOW)

    async def test_exists_fasle(self, get_fakeUOW: FakeUOWContext):
        async with get_fakeUOW as uow:
            assert not await uow.token.exists(jti=self.data_jti['jti'])

        assertional_session_aexit(get_fakeUOW)
