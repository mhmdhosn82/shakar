from __future__ import annotations

from pydantic import BaseModel, Field

from app.schemas.common import APIModel


class LoginRequest(BaseModel):
    username: str = Field(..., description="Username or email")
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class Token(APIModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
