from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel

from app.schemas.common import APIModel


class PermissionBase(BaseModel):
    resource: str
    action: str
    description: str | None = None


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(BaseModel):
    resource: str | None = None
    action: str | None = None
    description: str | None = None


class PermissionRead(APIModel):
    id: UUID
    resource: str
    action: str
    description: str | None = None


class RoleBase(BaseModel):
    name: str
    code: str
    description: str | None = None


class RoleCreate(RoleBase):
    permission_ids: list[UUID] = []


class RoleUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    description: str | None = None
    permission_ids: list[UUID] | None = None


class RoleRead(APIModel):
    id: UUID
    name: str
    code: str
    description: str | None = None


class UserBase(BaseModel):
    email: str
    username: str
    full_name: str | None = None
    phone: str | None = None
    role_id: UUID | None = None
    branch_id: UUID | None = None
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: str | None = None
    username: str | None = None
    password: str | None = None
    full_name: str | None = None
    phone: str | None = None
    role_id: UUID | None = None
    branch_id: UUID | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None


class UserRead(APIModel):
    id: UUID
    email: str
    username: str
    full_name: str | None = None
    phone: str | None = None
    role_id: UUID | None = None
    branch_id: UUID | None = None
    is_active: bool
    is_superuser: bool
