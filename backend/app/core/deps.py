from __future__ import annotations

from collections.abc import AsyncGenerator, Callable
from typing import Any
from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import get_settings
from app.core.database import get_db as get_db_session
from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.core.security import verify_token
from app.models.user import Role, User

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_db_session():
        yield session


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    payload = verify_token(token, expected_type="access")
    user_id = payload.get("sub")
    stmt = (
        select(User)
        .options(selectinload(User.role).selectinload(Role.permissions))
        .where(User.id == UUID(user_id), User.is_deleted.is_(False))
    )
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None:
        raise UnauthorizedError("User not found")
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise ForbiddenError("Inactive user")
    return current_user


def require_permission(resource: str, action: str) -> Callable[[User], User]:
    async def dependency(current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.is_superuser:
            return current_user
        if current_user.role is None:
            raise ForbiddenError("Role is required for this action")
        permissions = {(permission.resource, permission.action) for permission in current_user.role.permissions}
        if (resource, action) not in permissions and (resource, "manage") not in permissions:
            raise ForbiddenError(f"Missing permission: {resource}:{action}")
        return current_user

    return dependency
