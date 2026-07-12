from __future__ import annotations

from math import ceil
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginationMeta(BaseModel):
    total: int
    page: int
    page_size: int
    pages: int


def build_pagination_meta(total: int, page: int, page_size: int) -> PaginationMeta:
    return PaginationMeta(total=total, page=page, page_size=page_size, pages=max(1, ceil(total / page_size)) if page_size else 1)
