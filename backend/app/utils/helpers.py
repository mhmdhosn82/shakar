from math import ceil
from typing import Any, Sequence, TypeVar
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_active_user, get_db, require_permission
from app.core.exceptions import NotFoundError
from app.schemas.common import PaginatedResponse, SuccessResponse

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")
ReadSchemaType = TypeVar("ReadSchemaType")


class CRUDService:
    def __init__(self, model: type[ModelType], search_fields: Sequence[str] = ()) -> None:
        self.model = model
        self.search_fields = tuple(search_fields)

    def _base_filters(self) -> list[Any]:
        if hasattr(self.model, "is_deleted"):
            return [getattr(self.model, "is_deleted").is_(False)]
        return []

    async def list(
        self,
        session: AsyncSession,
        *,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
    ) -> dict[str, Any]:
        filters = self._base_filters()
        if search and self.search_fields:
            search_filters = [getattr(self.model, field).ilike(f"%{search}%") for field in self.search_fields]
            filters.append(or_(*search_filters))

        stmt = select(self.model).where(*filters).order_by(getattr(self.model, "created_at", getattr(self.model, "id")))
        total_stmt = select(func.count()).select_from(stmt.order_by(None).subquery())
        total = int((await session.execute(total_stmt)).scalar_one())
        result = await session.execute(stmt.offset((page - 1) * page_size).limit(page_size))
        items = result.scalars().all()
        pages = max(1, ceil(total / page_size)) if page_size else 1
        return {"items": items, "total": total, "page": page, "page_size": page_size, "pages": pages}

    async def get(self, session: AsyncSession, object_id: UUID) -> ModelType:
        filters = self._base_filters()
        stmt = select(self.model).where(getattr(self.model, "id") == object_id, *filters)
        result = await session.execute(stmt)
        instance = result.scalar_one_or_none()
        if instance is None:
            raise NotFoundError(f"{self.model.__name__} not found")
        return instance

    async def create(self, session: AsyncSession, payload: dict[str, Any]) -> ModelType:
        instance = self.model(**payload)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance

    async def update(self, session: AsyncSession, object_id: UUID, payload: dict[str, Any]) -> ModelType:
        instance = await self.get(session, object_id)
        for field, value in payload.items():
            setattr(instance, field, value)
        await session.commit()
        await session.refresh(instance)
        return instance

    async def delete(self, session: AsyncSession, object_id: UUID) -> None:
        instance = await self.get(session, object_id)
        if hasattr(instance, "is_deleted"):
            setattr(instance, "is_deleted", True)
            await session.commit()
            return
        await session.delete(instance)
        await session.commit()


def build_crud_router(
    *,
    service: CRUDService,
    create_schema: type[Any],
    update_schema: type[Any],
    read_schema: type[Any],
    resource: str,
) -> APIRouter:
    router = APIRouter()
    list_response = PaginatedResponse[read_schema]

    @router.get(
        "/",
        response_model=list_response,
        dependencies=[Depends(require_permission(resource, "read"))],
    )
    async def list_items(
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=20, ge=1, le=100),
        search: str | None = Query(default=None),
        _: Any = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_db),
    ) -> Any:
        return await service.list(db, page=page, page_size=page_size, search=search)

    @router.get(
        "/{item_id}",
        response_model=read_schema,
        dependencies=[Depends(require_permission(resource, "read"))],
    )
    async def get_item(
        item_id: UUID,
        _: Any = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_db),
    ) -> Any:
        return await service.get(db, item_id)

    @router.post(
        "/",
        response_model=read_schema,
        status_code=status.HTTP_201_CREATED,
        dependencies=[Depends(require_permission(resource, "create"))],
    )
    async def create_item(
        payload: create_schema,
        _: Any = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_db),
    ) -> Any:
        return await service.create(db, payload.model_dump(exclude_unset=True))

    @router.patch(
        "/{item_id}",
        response_model=read_schema,
        dependencies=[Depends(require_permission(resource, "update"))],
    )
    async def update_item(
        item_id: UUID,
        payload: update_schema,
        _: Any = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_db),
    ) -> Any:
        return await service.update(db, item_id, payload.model_dump(exclude_unset=True))

    @router.delete(
        "/{item_id}",
        response_model=SuccessResponse,
        dependencies=[Depends(require_permission(resource, "delete"))],
    )
    async def delete_item(
        item_id: UUID,
        _: Any = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_db),
    ) -> SuccessResponse:
        await service.delete(db, item_id)
        return SuccessResponse(detail=f"{service.model.__name__} deleted successfully")

    return router
