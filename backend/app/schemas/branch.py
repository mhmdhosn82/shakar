from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel

from app.schemas.common import APIModel


class BranchCreate(BaseModel):
    name: str
    code: str
    address: str | None = None
    phone: str | None = None
    city: str | None = None
    is_active: bool = True
    parent_id: UUID | None = None


class BranchUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    address: str | None = None
    phone: str | None = None
    city: str | None = None
    is_active: bool | None = None
    parent_id: UUID | None = None


class BranchRead(APIModel):
    id: UUID
    name: str
    code: str
    address: str | None = None
    phone: str | None = None
    city: str | None = None
    is_active: bool
    parent_id: UUID | None = None
