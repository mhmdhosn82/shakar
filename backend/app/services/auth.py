from __future__ import annotations

from datetime import timedelta

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.exceptions import UnauthorizedError
from app.core.security import create_access_token, create_refresh_token, verify_password
from app.models.user import User


class AuthService:
    async def authenticate_user(self, db: AsyncSession, username: str, password: str) -> User:
        stmt = select(User).where(
            or_(User.username == username, User.email == username),
            User.is_deleted.is_(False),
        )
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        if user is None or not verify_password(password, user.hashed_password):
            raise UnauthorizedError("Incorrect username or password")
        if not user.is_active:
            raise UnauthorizedError("Inactive user")
        return user

    async def login(self, db: AsyncSession, username: str, password: str) -> dict[str, str | int]:
        settings = get_settings()
        user = await self.authenticate_user(db, username, password)
        access_token = create_access_token(str(user.id))
        refresh_token = create_refresh_token(
            str(user.id), timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        }

    async def refresh(self, refresh_token: str) -> dict[str, str | int]:
        from app.core.security import verify_token

        settings = get_settings()
        payload = verify_token(refresh_token, expected_type="refresh")
        access_token = create_access_token(str(payload["sub"]))
        new_refresh_token = create_refresh_token(str(payload["sub"]))
        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        }


auth_service = AuthService()
