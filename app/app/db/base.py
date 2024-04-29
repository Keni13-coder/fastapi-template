from datetime import datetime
from typing import Annotated
import uuid

import pydantic
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, declared_attr
from sqlalchemy.inspection import inspect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import MetaData, text

from app.utils.const import DB_NAMING_CONVENTION


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    repr_cols_num = 3
    repr_cols = tuple()
    __serialize_class__ = dict

    def __repr__(self):
        """Relationships не используются в repr(), т.к. могут вести к неожиданным подгрузкам"""
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"

    def to_dict(self):
        if isinstance(self.__serialize_class__, dict):
            return {
                c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs
            }
        else:
            return self.__serialize_class__.model_validate(self, from_attributes=True)

    def to_dict_with_relationship(self, schema: pydantic.BaseModel):
        return schema.model_validate(self, from_attributes=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


created_at = Annotated[
    datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))
]
updated_at = Annotated[
    datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=text("TIMEZONE('utc', now())"),
    ),
]
is_active = Annotated[bool, mapped_column(default=True, doc="Активность")]
