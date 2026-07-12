from __future__ import annotations

from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestError
from app.core.security import get_password_hash
from app.models.user import Permission, Role, RolePermission, User
from app.utils.helpers import CRUDService


class UserService(CRUDService):
    async def create(self, session: AsyncSession, payload: dict) -> User:
        password = payload.pop("password")
        payload["hashed_password"] = get_password_hash(password)
        instance = self.model(**payload)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance

    async def update(self, session: AsyncSession, object_id: UUID, payload: dict) -> User:
        if "password" in payload:
            payload["hashed_password"] = get_password_hash(payload.pop("password"))
        return await super().update(session, object_id, payload)


class RoleService(CRUDService):
    async def create(self, session: AsyncSession, payload: dict) -> Role:
        permission_ids = payload.pop("permission_ids", [])
        role = self.model(**payload)
        session.add(role)
        await session.flush()
        for permission_id in permission_ids:
            session.add(RolePermission(role_id=role.id, permission_id=permission_id))
        await session.commit()
        await session.refresh(role)
        return role

    async def update(self, session: AsyncSession, object_id: UUID, payload: dict) -> Role:
        permission_ids = payload.pop("permission_ids", None)
        role = await super().update(session, object_id, payload)
        if permission_ids is not None:
            await session.execute(delete(RolePermission).where(RolePermission.role_id == role.id))
            for permission_id in permission_ids:
                session.add(RolePermission(role_id=role.id, permission_id=permission_id))
            await session.commit()
            await session.refresh(role)
        return role


class PermissionService(CRUDService):
    async def create(self, session: AsyncSession, payload: dict) -> Permission:
        if not payload.get("resource") or not payload.get("action"):
            raise BadRequestError("resource and action are required")
        return await super().create(session, payload)


user_service = UserService(User, search_fields=("email", "username", "full_name"))
role_service = RoleService(Role, search_fields=("name", "code"))
permission_service = PermissionService(Permission, search_fields=("resource", "action"))
