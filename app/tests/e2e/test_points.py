import httpx
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.config import settings
from app.schemas.user import CreateUser


@pytest.mark.usefixtures("prepare_database")  # , 'clear_user_db'
class TestUserPoint:
    async def test_register(
        self,
        ac: httpx.AsyncClient,
        create_data_user: CreateUser,
        get_session: AsyncSession,
    ):
        response = await ac.post(
            url=f"{settings.api_v1_str}/user/register/",
            content=create_data_user.model_dump_json().encode(),
        )
        assert response.status_code == 201
        users = await get_session.execute(text("SELECT id FROM public.user"))
        assert users.scalars().all()

    async def test_login(self, ac: httpx.AsyncClient, create_data_user: CreateUser):
        response = await ac.post(
            url=f"{settings.api_v1_str}/user/login/", data=create_data_user.model_dump()
        )
        assert response.status_code == 200
        assert response.cookies["token"]
