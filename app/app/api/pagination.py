from typing import Generic, TypeVar

from fastapi import Query, HTTPException
from pydantic import BaseModel


T = TypeVar("T")


class PaginationParams(BaseModel):
    page: int = Query(1, gt=0, description="Номер страницы")
    page_size: int = Query(
        10, gt=0, lt=101, description="Количество элементов на странице"
    )


class BasePaginationResponse(BaseModel, Generic[T]):
    total_items: int
    total_pages: int
    page: int
    page_size: int
    data: list[T]


class Paginator(Generic[T]):
    def __init__(self, data: list[T], pagination_params: PaginationParams):
        self.data = data
        self.pagination_params = pagination_params

    def paginate(self) -> list[T]:
        start = (self.pagination_params.page - 1) * self.pagination_params.page_size
        end = start + self.pagination_params.page_size
        return self.data[start:end]

    def get_response(self) -> BasePaginationResponse[T]:
        total_items = len(self.data)
        total_pages = (total_items // self.pagination_params.page_size) + (
            1 if total_items % self.pagination_params.page_size else 0
        )
        if self.pagination_params.page > total_pages != 0:
            raise HTTPException(status_code=404, detail="Страница не найдена")

        return BasePaginationResponse[T](
            total_items=total_items,
            total_pages=total_pages,
            page=self.pagination_params.page,
            page_size=self.pagination_params.page_size,
            data=self.paginate(),
        )
