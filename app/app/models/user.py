import enum
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from app.db.base import Base
from app.schemas.user import ResponseUserSchema
from app.db import base


from app.utils.const import UserRole


class User(Base):
    """Модель пользователя"""

    login: Mapped[str] = mapped_column(String(255), doc="Логин", unique=True)
    is_authenticated: Mapped[bool] = mapped_column(default=False)
    role: Mapped[UserRole] = mapped_column(
        doc="Роль пользователя", default=UserRole.user
    )
    password: Mapped[str] = mapped_column(String(80), doc="Пароль")
    created_at: Mapped[base.created_at]
    updated_at: Mapped[base.updated_at]
    is_active: Mapped[base.is_active]
