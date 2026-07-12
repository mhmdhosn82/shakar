from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel

from app.schemas.common import APIModel


class AuditLogCreate(BaseModel):
    user_id: UUID | None = None
    action: str
    resource_type: str
    resource_id: str | None = None
    old_values: dict | None = None
    new_values: dict | None = None
    ip_address: str | None = None
    user_agent: str | None = None
    branch_id: UUID | None = None


class AuditLogUpdate(BaseModel):
    user_id: UUID | None = None
    action: str | None = None
    resource_type: str | None = None
    resource_id: str | None = None
    old_values: dict | None = None
    new_values: dict | None = None
    ip_address: str | None = None
    user_agent: str | None = None
    branch_id: UUID | None = None


class AuditLogRead(APIModel):
    id: UUID
    user_id: UUID | None = None
    action: str
    resource_type: str
    resource_id: str | None = None
    old_values: dict | None = None
    new_values: dict | None = None
    ip_address: str | None = None
    user_agent: str | None = None
    branch_id: UUID | None = None
