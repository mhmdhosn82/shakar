from __future__ import annotations

import uuid

from sqlalchemy import Boolean, ForeignKey, String, Text, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import TimestampedUUIDModel


class Branch(TimestampedUUIDModel):
    __tablename__ = "branches"

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=text("true"), nullable=False)
    parent_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("branches.id"), nullable=True)

    parent: Mapped[Branch | None] = relationship(remote_side="Branch.id", back_populates="children")
    children: Mapped[list[Branch]] = relationship(back_populates="parent")
    users: Mapped[list["User"]] = relationship(back_populates="branch")
    warehouses: Mapped[list["Warehouse"]] = relationship(back_populates="branch")

    def __repr__(self) -> str:
        return f"<Branch(code={self.code!r}, name={self.name!r})>"


