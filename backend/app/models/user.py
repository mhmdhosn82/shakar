from __future__ import annotations

import uuid

from sqlalchemy import Boolean, ForeignKey, String, Text, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import TimestampedUUIDModel


class RolePermission(TimestampedUUIDModel):
    __tablename__ = "role_permissions"

    role_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    permission_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False)

    role: Mapped["Role"] = relationship(back_populates="role_permissions")
    permission: Mapped["Permission"] = relationship(back_populates="role_permissions")

    def __repr__(self) -> str:
        return f"<RolePermission(role_id={self.role_id}, permission_id={self.permission_id})>"


class Role(TimestampedUUIDModel):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    users: Mapped[list["User"]] = relationship(back_populates="role")
    role_permissions: Mapped[list[RolePermission]] = relationship(back_populates="role", cascade="all, delete-orphan")
    permissions: Mapped[list["Permission"]] = relationship(
        secondary="role_permissions",
        primaryjoin="Role.id == RolePermission.role_id",
        secondaryjoin="Permission.id == RolePermission.permission_id",
        viewonly=True,
    )

    def __repr__(self) -> str:
        return f"<Role(code={self.code!r}, name={self.name!r})>"


class Permission(TimestampedUUIDModel):
    __tablename__ = "permissions"

    resource: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    role_permissions: Mapped[list[RolePermission]] = relationship(back_populates="permission", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Permission(resource={self.resource!r}, action={self.action!r})>"


class User(TimestampedUUIDModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    role_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("roles.id"), nullable=True, index=True)
    branch_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("branches.id"), nullable=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=text("true"), nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text("false"), nullable=False)

    role: Mapped[Role | None] = relationship(back_populates="users")
    branch: Mapped["Branch"] = relationship(back_populates="users")

    def __repr__(self) -> str:
        return f"<User(username={self.username!r}, email={self.email!r})>"


