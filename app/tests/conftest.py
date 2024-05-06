import asyncio
from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.db.session import engine, async_sessionmaker
from app.db.base import Base
from app.models.user import User
from app.models.token import Token
from app.core.config import settings

from tests.async_database import create_database, database_exists
from tests.fixture_for_schemas.user import (
    create_data_user,
    update_data_user_login,
    update_data_user_password,
)
from tests.fixture_for_schemas.token import create_data_token, update_data_token
from tests.fixture_for_schemas.jwt import create_jwt_access, create_jwt_refresh

from app.services.subdomain.jwt_service import ABCJWT, JWTService
from app.services.token import ABCTokenService, TokenService, TokenSchema
from app.services.subdomain.serialize_service import TokenEntitySerializer


# loop region
@pytest.fixture(scope="session")
def event_loop():
    try:
        policy = asyncio.get_event_loop_policy()
        loop = policy.new_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# endregion


# data bases region


@pytest.fixture(scope="session")
async def prepare_database():
    assert settings.MODE == "test"
    statement = text("DROP SCHEMA IF EXISTS public CASCADE;")

    if not await database_exists(settings.postgres_url):
        await create_database(settings.postgres_url)

    async with engine.begin() as conn:
        await conn.execute(statement)
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS public;"))

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.execute(statement)

    await engine.dispose()


@pytest.fixture(scope="class")
async def clear_user_db(get_session: AsyncSession):
    ...
    yield
    await get_session.execute(text("TRUNCATE public.user"))
    await get_session.commit()


@pytest.fixture
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_sessionmaker(engine, expire_on_commit=False)() as session:
        yield session
        await session.rollback()
        await session.close()


# endregion


# class region
@pytest.fixture(scope="class")
def token_service() -> ABCTokenService:
    return TokenService(
        jwt_service=JWTService,
        serializer=TokenEntitySerializer(serialize_schema=TokenSchema),
    )


# endregion


# settings region
@pytest.fixture(scope="class")
def high_lifetime():
    settings.expired_access = 20


@pytest.fixture
def last_time_refresh():
    settings.expired_access = 20
    yield
    settings.expired_access = 0


@pytest.fixture(scope="class")
def low_lifetime():
    settings.expired_access = 0
    settings.expired_refresh = 10


# endregion
