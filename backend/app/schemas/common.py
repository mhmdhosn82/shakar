from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class APIModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PaginatedResponse(APIModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    pages: int


class SuccessResponse(APIModel):
    success: bool = True
    detail: str = "Success"


class ErrorResponse(APIModel):
    success: bool = False
    detail: str
    error: str | None = None
