import abc
from typing import Any

from app.repositories.base import ABCRepository


class ABCUoW(abc.ABC):
    __abc_class_repository = ABCRepository

    @abc.abstractmethod
    def __init__(self, session) -> None:
        raise NotImplementedError

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "session" or isinstance(__value, self.__abc_class_repository):
            super().__setattr__(__name, __value)
        else:
            raise TypeError(
                f"Не соответсвие типов класса {__name=} -> должен быть дочерним класса {self.__abc_class_repository}"
            )

    def __getattr__(self, name):
        raise ValueError(f"An attribute with a name {name} does not exist")

    @abc.abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def close(self):
        raise NotImplementedError


class DefaultSessionPackMixin:

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def close(self):
        await self.session.close()
