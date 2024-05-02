from uuid import UUID
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
import abc
import uuid

from pydantic import BaseModel
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base

ResponseModelType = TypeVar("ResponseModelType", bound=Union[Base, dict])

CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class ABCRepository(
    abc.ABC, Generic[ResponseModelType, CreateSchemaType, UpdateSchemaType]
):

    _model = None

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    @abc.abstractmethod
    async def create(
        self, obj_in: Union[CreateSchemaType, Dict[str, Any]]
    ) -> ResponseModelType:
        raise NotImplementedError

    @abc.abstractmethod
    async def get(
        self,
        **kwargs,
    ) -> Optional[ResponseModelType]:
        raise NotImplementedError

    @abc.abstractmethod
    async def list(
        self, offset: int = 0, limit: int = 1000, **kwargs
    ) -> Optional[List[ResponseModelType]]:
        raise NotImplementedError

    @abc.abstractmethod
    async def update(
        self,
        *,
        obj_id: UUID,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ResponseModelType:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, obj_id: UUID, **kwargs) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def exists(self, **kwargs) -> bool:
        raise NotImplementedError


class RepositoryBase(
    ABCRepository[ResponseModelType, CreateSchemaType, UpdateSchemaType]
):
    """Репозиторий с базовым CRUD"""

    async def create(
        self,
        obj_in: Union[CreateSchemaType, Dict[str, Any]],
    ) -> ResponseModelType:
        if isinstance(obj_in, dict):
            create_data = obj_in
        else:
            create_data = obj_in.model_dump(exclude_unset=True)
        statement = insert(self._model).values(**create_data).returning(self._model)

        res = await self.session.execute(statement)
        return res.scalar_one()

    async def get(
        self,
        **kwargs,
    ) -> Optional[ResponseModelType]:
        statement = select(self._model).filter_by(**kwargs)
        res = await self.session.execute(statement)

        return res.scalar_one_or_none()

    async def list(
        self, offset: int = 0, limit: int = 1000, **kwargs
    ) -> Optional[List[ResponseModelType]]:
        statement = select(self._model).filter_by(**kwargs).offset(offset).limit(limit)
        res = await self.session.execute(statement)
        return res.scalars().all()

    async def update(
        self, obj_in: Union[UpdateSchemaType, Dict[str, Any]], **kwargs
    ) -> Optional[ResponseModelType]:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        statement = (
            update(self._model)
            .filter_by(**kwargs)
            .values(**update_data)
            .returning(self._model)
        )
        update_model = await self.session.execute(statement)

        return update_model.scalar_one_or_none()

    async def delete(self, **kwargs) -> None:
        statement = delete(self._model).filter_by(**kwargs)
        await self.session.execute(statement)

    async def exists(self, **kwargs) -> bool:
        try:
            statement = select(self._model).filter_by(**kwargs)
            res = await self.session.execute(statement)
            res.scalar_one()
            return True
        except NoResultFound:
            return False
        except MultipleResultsFound:
            return False


class TestRepositoryBase(
    ABCRepository[ResponseModelType, CreateSchemaType, UpdateSchemaType]
):

    async def create(
        self, obj_in: Union[CreateSchemaType, Dict[str, Any]]
    ) -> ResponseModelType:
        if isinstance(obj_in, dict):
            create_data = obj_in
        else:
            create_data = obj_in.model_dump(exclude_unset=True)
        create_data["id"] = uuid.uuid4()
        self._model.append(create_data)
        return self._model[-1]

    async def get(
        self,
        **kwargs,
    ) -> Optional[ResponseModelType]:
        for data in self._model:
            for value in data.values():
                if value in kwargs.values():
                    return data
        return

    async def list(
        self, offset: int = 0, limit: int = 1000, **kwargs
    ) -> Optional[List[ResponseModelType]]:
        resul_list = []
        for data in self._model:
            for value in data.values():
                if value in kwargs.values():
                    resul_list += [data]
        resul_list = resul_list if resul_list else self._model

        return resul_list[offset:limit]

    async def update(
        self, obj_in: Union[UpdateSchemaType, Dict[str, Any]], **kwargs
    ) -> ResponseModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for data in self._model:
            for value in data.values():
                if value in kwargs.values():
                    data.update(update_data)
                    return data
        return

    async def delete(self, **kwargs) -> None:
        for data in self._model:
            for value in data.values():
                if value in kwargs.values():
                    self._model.remove(data)
                    return

    async def exists(self, **kwargs) -> bool:
        for data in self._model:
            for value in data.values():
                if value in kwargs.values():
                    return True

        return False
