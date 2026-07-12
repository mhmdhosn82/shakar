from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_active_user, get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, RefreshTokenRequest, Token
from app.schemas.user import UserRead
from app.services.auth import auth_service

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)) -> Token:
    return Token(**await auth_service.login(db, payload.username, payload.password))


@router.post("/refresh", response_model=Token)
async def refresh_token(payload: RefreshTokenRequest) -> Token:
    return Token(**await auth_service.refresh(payload.refresh_token))


@router.get("/me", response_model=UserRead)
async def read_current_user(current_user: User = Depends(get_current_active_user)) -> UserRead:
    return UserRead.model_validate(current_user)
