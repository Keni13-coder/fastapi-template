from typing import Generic, TypeVar

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import RepositoryBase, CreateSchemaType, UpdateSchemaType
from sqlalchemy import insert, select, update, delete
from tests.integration.conftest import CreateUser, UpdateUser

RepositoryClass = TypeVar("RepositoryClass", bound=RepositoryBase)


class RepositoryIntegrationTest(Generic[CreateSchemaType, UpdateSchemaType]):
    _result_data = None

    def __init__(
        self,
        repository: RepositoryClass,
        get_session: AsyncSession,
        CreateSchema: CreateSchemaType,
        UpdateSchema: UpdateSchemaType,
    ) -> None:
        self.test_repository = repository
        self.session = get_session
        self.create_data_schema = CreateSchema
        self.update_data_schema = UpdateSchema

    async def create(self):
        result = await self.test_repository.create(self.create_data_schema)
        assert result

        stmt = select(self.test_repository._model)
        result = await self.session.execute(statement=stmt)
        result = result.scalar_one().to_dict()
        assert result
        self._result_data = result
        return result

    async def get(self):
        assert self._result_data
        result = await self.test_repository.get(id=self._result_data.id)
        assert result

        return result

    async def list(self):
        result = await self.test_repository.list()
        assert len(result) == 1

        return result

    async def update(self):
        old_data = await self.get()

        result = await self.test_repository.update(
            id=self._result_data.id, obj_in=self.update_data_schema
        )

        assert result
        stmt = select(self.test_repository._model)
        result = await self.session.execute(statement=stmt)
        result = result.scalar_one()
        new_data = result.to_dict()
        assert result
        assert old_data != new_data
        self._result_data = new_data

        return new_data

    async def delete(self):
        await self.test_repository.delete(id=self._result_data.id)
        stmt = select(self.test_repository._model).filter_by(id=self._result_data.id)
        result = await self.session.execute(statement=stmt)
        result = result.scalars().all()

        assert not result

    async def exists_true(self):
        result = await self.test_repository.exists(id=self._result_data.id)
        assert result

    async def exists_false(self):
        result = await self.test_repository.exists(id=self._result_data.id)
        assert not result


class TestUserIntegration(RepositoryIntegrationTest[CreateUser, UpdateUser]): ...
