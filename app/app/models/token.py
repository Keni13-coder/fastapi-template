import uuid
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app.db import base
from app.schemas.token import TokenSchema
from app.db.base import Base


class Token(Base):
    jti: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    user_uid: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), index=True, nullable=False
    )
    device_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    access_nfb: Mapped[datetime]
    is_active: Mapped[base.is_active]

    __serialize_class__ = TokenSchema
