from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit import AuditLog
from app.utils.helpers import CRUDService


audit_log_service = CRUDService(AuditLog, search_fields=("action", "resource_type", "resource_id", "ip_address"))


async def log_action(session: AsyncSession, payload: dict) -> AuditLog:
    instance = AuditLog(**payload)
    session.add(instance)
    await session.commit()
    await session.refresh(instance)
    return instance
