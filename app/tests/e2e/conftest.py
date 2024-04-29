from typing import AsyncGenerator

import pytest
import httpx

from app.main import app
from tests.conftest import event_loop




@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
