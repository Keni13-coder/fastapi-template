import asyncio
from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from tests.async_database import create_database, database_exists
from app.db.session import engine, async_session_maker
from app.db.base import Base
from app.core.config import settings

from tests.fixture_for_schemas.user import (
    create_data_user,
    update_data_user_login,
    update_data_user_password,
)
from tests.fixture_for_schemas.token import create_data_token, update_data_token
from tests.fixture_for_schemas.jwt import create_jwt_access, create_jwt_refresh


@pytest.fixture(scope="session")
def event_loop(request):
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
async def get_session(event_loop):
    session = async_session_maker()
    yield session
    await session.rollback()
    await session.close()


@pytest.fixture(scope="session")
async def prepare_database():
    assert settings.MODE == "test"
    if not await database_exists(settings.postgres_url):
        await create_database(settings.postgres_url)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()
