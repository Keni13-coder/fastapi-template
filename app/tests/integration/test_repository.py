import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.repositories.user import RepositoryUser
from app.schemas.user import CreateUser


@pytest.mark.usefixtures("prepare_database")
class TestUserIntegration:
    """
    Тестирование базового функионала классов репозиторий
    """

    user = {"model": ""}

    async def test_create(
        self,
        get_session: AsyncSession,
        create_data_user: CreateUser,
        repository_user: RepositoryUser,
    ):
        user = await repository_user.create(
            obj_in=create_data_user.model_dump(exclude={"confirm_password"})
        )
        await get_session.commit()
        assert user
        self.user["model"] = user

    async def test_get(self, repository_user: RepositoryUser):
        assert await repository_user.get(id=self.user["model"].id)

    async def test_list(self, repository_user: RepositoryUser):
        assert await repository_user.list()

    @pytest.mark.parametrize(
        "data_user",
        ["update_data_user_password", "update_data_user_login"],
        indirect=True,
    )
    async def test_update(
        self, get_session: AsyncSession, repository_user: RepositoryUser, data_user
    ):
        old_user = self.user["model"]
        upgrade_user = await repository_user.update(
            id=self.user["model"].id, obj_in=data_user
        )
        await get_session.commit()

        assert upgrade_user
        assert old_user != upgrade_user

    async def test_exists_true(self, repository_user: RepositoryUser):
        assert await repository_user.exists(id=self.user["model"].id)

    async def test_delete(
        self, get_session: AsyncSession, repository_user: RepositoryUser
    ):
        await repository_user.delete(id=self.user["model"].id)
        await get_session.commit()
        statement = text(f"SELECT * FROM public.user WHERE id=:id")
        result = await get_session.execute(
            statement=statement, params=dict(id=self.user["model"].id)
        )
        assert result.scalar_one_or_none() is None

    async def test_exists_false(self, repository_user: RepositoryUser):
        assert not await repository_user.exists(id=self.user["model"].id)
