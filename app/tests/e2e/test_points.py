import httpx
from app.core.config import settings


class TestPoint:
    async def test_register(self, ac: httpx.AsyncClient):
        response = await ac.post(url=f"{settings.api_v1_str}/point/test-annotation/")
        assert response.status_code == 200
