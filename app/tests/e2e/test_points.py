import json
import httpx
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.config import settings
from app.schemas.user import CreateUser


@pytest.mark.usefixtures("prepare_database", "high_lifetime")
class TestUserPoint:

    tokens = {}

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
        response_data = json.loads(response.read().decode())["detail"][0]
        assert response_data
        self.tokens.update({"access": response_data["access_token"]})

    async def test_get_all(self, ac: httpx.AsyncClient):
        response = await ac.get(url=f"{settings.api_v1_str}/user/get-all/")
        assert response.status_code == 200
        response_data = json.loads(response.read().decode())
        assert response_data["detail"]
        null_response = await ac.get(
            url=f"{settings.api_v1_str}/user/get-all/", params={"offset": 1}
        )
        response_data_null = json.loads(null_response.read().decode())
        assert response.status_code == 200
        assert not response_data_null["detail"]

    async def test_get_one(self, ac: httpx.AsyncClient):
        headers = {"authorization": self.tokens["access"]}
        response = await ac.get(
            url=f"{settings.api_v1_str}/user/get-one/", headers=headers
        )
        assert response.status_code == 200
        response_data = json.loads(response.read().decode())
        assert response_data["detail"]
