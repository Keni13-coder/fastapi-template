from typing import Type

import pytest
from tests.integration.utils import RepositoryIntegrationTest


@pytest.mark.parametrize("starter_repository", ["start_user"], indirect=True)
class TestStartIntegration:
    """
    Тестирование базового функионала классов репозиторий
    """

    async def test_create(self, starter_repository: Type[RepositoryIntegrationTest]):
        await starter_repository.create()

    async def test_get(self, starter_repository: Type[RepositoryIntegrationTest]):
        await starter_repository.get()

    async def test_list(self, starter_repository: Type[RepositoryIntegrationTest]):
        await starter_repository.list()

    async def test_update(self, starter_repository: Type[RepositoryIntegrationTest]):
        await starter_repository.update()

    async def test_exists_true(
        self, starter_repository: Type[RepositoryIntegrationTest]
    ):
        await starter_repository.exists_true()

    async def test_delete(self, starter_repository: Type[RepositoryIntegrationTest]):
        await starter_repository.delete()

    async def test_exists_false(
        self, starter_repository: Type[RepositoryIntegrationTest]
    ):
        await starter_repository.exists_false()
