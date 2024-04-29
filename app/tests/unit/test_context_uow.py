import pytest
from app.schemas.user import CreateUser, UpdateLogin, СhangePassword
from tests.unit.utils import assertional_session_aexit
from tests.unit.conftest import FakeUOWContext


class TestContextUser:

    async def test_create_user(
        self, get_fakeUOW: FakeUOWContext, create_data_user: CreateUser
    ):
        async with get_fakeUOW as uow:

            data = create_data_user.model_dump()
            data["id"] = "1"
            user = await uow.user.create(obj_in=data)
            await uow.commit()

            assert get_fakeUOW.session.is_commit
            assert user
            assert len(uow.user._model) == 1

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
            user = await uow.user.update(id="1", obj_in=update_data_user_login)
            await uow.commit()

            assert get_fakeUOW.session.is_commit
            assert user
            assert user["login"] == "newlogin"

        assertional_session_aexit(get_fakeUOW)

    async def test_update_user_password(
        self, get_fakeUOW: FakeUOWContext, update_data_user_password: СhangePassword
    ):

        async with get_fakeUOW as uow:
            user = await uow.user.update(id="1", obj_in=update_data_user_password)
            await uow.commit()

            assert get_fakeUOW.session.is_commit
            assert user
            assert user["password"] == "1414"

        assertional_session_aexit(get_fakeUOW)

    async def test_exists_true(self, get_fakeUOW: FakeUOWContext):
        async with get_fakeUOW as uow:
            result = await uow.user.exists(id="1")
            assert result

        assertional_session_aexit(get_fakeUOW)

    async def test_delete_user(self, get_fakeUOW: FakeUOWContext):
        async with get_fakeUOW as uow:
            await uow.user.delete(id="1")
            await uow.commit()

            assert get_fakeUOW.session.is_commit

            assert uow.user._model == []

        assertional_session_aexit(get_fakeUOW)

    async def test_exists_fasle(self, get_fakeUOW: FakeUOWContext):
        async with get_fakeUOW as uow:
            result = await uow.user.exists(id="1")
            assert not result

        assertional_session_aexit(get_fakeUOW)


@pytest.fixture(scope="class")
def data_jti():
    __jti = ""

    def _jti(jti=""):
        global __jti
        if jti:
            __jti = jti
            return jti
        else:
            return __jti

    yield _jti

    __jti = ""


class TestContextToken:

    async def test_create_token(
        self, get_fakeUOW: FakeUOWContext, create_data_token, data_jti
    ):
        async with get_fakeUOW as uow:
            create_data_token["id"] = "1"
            token = await uow.token.create(create_data_token)
            assert token
            assert len(uow.token._model) == 1

        assertional_session_aexit(get_fakeUOW)
        assert data_jti(create_data_token["jti"])

    async def test_get_token(self, get_fakeUOW: FakeUOWContext, data_jti):
        async with get_fakeUOW as uow:
            token = await uow.token.get(jti=data_jti())
            assert token

        assertional_session_aexit(get_fakeUOW)

    async def test_get_list_token(self, get_fakeUOW: FakeUOWContext):
        async with get_fakeUOW as uow:
            tokens = await uow.token.list()

            assert tokens
            assert len(tokens) == 1

        assertional_session_aexit(get_fakeUOW)

    async def test_update_token(
        self, get_fakeUOW: FakeUOWContext, update_data_token, data_jti
    ):
        async with get_fakeUOW as uow:
            token = await uow.token.update(obj_id="1", obj_in=update_data_token)
            assert token
            assert token["jti"] != data_jti()
            assert data_jti(token["jti"])
        assertional_session_aexit(get_fakeUOW)

    async def test_exists_true(self, get_fakeUOW: FakeUOWContext, data_jti):

        async with get_fakeUOW as uow:
            assert await uow.token.exists(jti=data_jti())

        assertional_session_aexit(get_fakeUOW)

    async def test_delete_token(self, get_fakeUOW: FakeUOWContext):
        async with get_fakeUOW as uow:
            await uow.token.delete(obj_id="1")
            assert uow.token._model == []

        assertional_session_aexit(get_fakeUOW)

    async def test_exists_fasle(self, get_fakeUOW: FakeUOWContext, data_jti):
        async with get_fakeUOW as uow:
            assert not await uow.token.exists(jti=data_jti())

        assertional_session_aexit(get_fakeUOW)
