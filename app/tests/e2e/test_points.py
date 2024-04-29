import httpx
import pytest
from app.core.config import settings


@pytest.mark.usefixtures("prepare_database")
class TestPoint:
    async def test_register(self, ac: httpx.AsyncClient):
        response = await ac.post(url=f"{settings.api_v1_str}/point/test-annotation/")
        assert response.status_code == 200
