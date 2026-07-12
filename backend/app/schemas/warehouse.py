from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel

from app.models.warehouse import StockMovementType
from app.schemas.common import APIModel


class WarehouseCreate(BaseModel):
    name: str
    code: str
    branch_id: UUID
    address: str | None = None
    is_active: bool = True


class WarehouseUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    branch_id: UUID | None = None
    address: str | None = None
    is_active: bool | None = None


class WarehouseRead(APIModel):
    id: UUID
    name: str
    code: str
    branch_id: UUID
    address: str | None = None
    is_active: bool


class StockCreate(BaseModel):
    product_id: UUID
    variant_id: UUID | None = None
    warehouse_id: UUID
    branch_id: UUID | None = None
    quantity: int = 0
    reserved_quantity: int = 0


class StockUpdate(BaseModel):
    product_id: UUID | None = None
    variant_id: UUID | None = None
    warehouse_id: UUID | None = None
    branch_id: UUID | None = None
    quantity: int | None = None
    reserved_quantity: int | None = None


class StockRead(APIModel):
    id: UUID
    product_id: UUID
    variant_id: UUID | None = None
    warehouse_id: UUID
    branch_id: UUID | None = None
    quantity: int
    reserved_quantity: int


class StockMovementCreate(BaseModel):
    product_id: UUID
    variant_id: UUID | None = None
    warehouse_id: UUID
    branch_id: UUID | None = None
    movement_type: StockMovementType
    quantity: int
    reference_id: UUID | None = None
    reference_type: str | None = None
    notes: str | None = None
    created_by: UUID | None = None


class StockMovementUpdate(BaseModel):
    product_id: UUID | None = None
    variant_id: UUID | None = None
    warehouse_id: UUID | None = None
    branch_id: UUID | None = None
    movement_type: StockMovementType | None = None
    quantity: int | None = None
    reference_id: UUID | None = None
    reference_type: str | None = None
    notes: str | None = None
    created_by: UUID | None = None


class StockMovementRead(APIModel):
    id: UUID
    product_id: UUID
    variant_id: UUID | None = None
    warehouse_id: UUID
    branch_id: UUID | None = None
    movement_type: StockMovementType
    quantity: int
    reference_id: UUID | None = None
    reference_type: str | None = None
    notes: str | None = None
    created_by: UUID | None = None
