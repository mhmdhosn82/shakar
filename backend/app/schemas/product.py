from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.models.product import ImeiStatus, ProductType
from app.schemas.common import APIModel


class CategoryCreate(BaseModel):
    name: str
    code: str
    parent_id: UUID | None = None
    description: str | None = None


class CategoryUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    parent_id: UUID | None = None
    description: str | None = None


class CategoryRead(APIModel):
    id: UUID
    name: str
    code: str
    parent_id: UUID | None = None
    description: str | None = None


class BrandCreate(BaseModel):
    name: str
    code: str
    country_of_origin: str | None = None
    description: str | None = None


class BrandUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    country_of_origin: str | None = None
    description: str | None = None


class BrandRead(APIModel):
    id: UUID
    name: str
    code: str
    country_of_origin: str | None = None
    description: str | None = None


class ProductCreate(BaseModel):
    sku: str
    barcode: str | None = None
    name: str
    category_id: UUID | None = None
    brand_id: UUID | None = None
    branch_id: UUID | None = None
    description: str | None = None
    product_type: ProductType = ProductType.other
    unit: str = "piece"
    min_stock_alert: int = 0
    is_active: bool = True


class ProductUpdate(BaseModel):
    sku: str | None = None
    barcode: str | None = None
    name: str | None = None
    category_id: UUID | None = None
    brand_id: UUID | None = None
    branch_id: UUID | None = None
    description: str | None = None
    product_type: ProductType | None = None
    unit: str | None = None
    min_stock_alert: int | None = None
    is_active: bool | None = None


class ProductRead(APIModel):
    id: UUID
    sku: str
    barcode: str | None = None
    name: str
    category_id: UUID | None = None
    brand_id: UUID | None = None
    branch_id: UUID | None = None
    description: str | None = None
    product_type: ProductType
    unit: str
    min_stock_alert: int
    is_active: bool


class ProductVariantCreate(BaseModel):
    product_id: UUID
    color: str | None = None
    storage_capacity: str | None = None
    ram: str | None = None
    attributes: dict | None = None
    sku_suffix: str | None = None
    extra_price: Decimal = Decimal("0")


class ProductVariantUpdate(BaseModel):
    product_id: UUID | None = None
    color: str | None = None
    storage_capacity: str | None = None
    ram: str | None = None
    attributes: dict | None = None
    sku_suffix: str | None = None
    extra_price: Decimal | None = None


class ProductVariantRead(APIModel):
    id: UUID
    product_id: UUID
    color: str | None = None
    storage_capacity: str | None = None
    ram: str | None = None
    attributes: dict | None = None
    sku_suffix: str | None = None
    extra_price: Decimal


class IMEIItemCreate(BaseModel):
    product_id: UUID
    variant_id: UUID | None = None
    branch_id: UUID | None = None
    imei: str
    purchase_invoice_item_id: UUID | None = None
    sales_invoice_item_id: UUID | None = None
    status: ImeiStatus = ImeiStatus.in_stock
    warranty_expires_at: datetime | None = None


class IMEIItemUpdate(BaseModel):
    product_id: UUID | None = None
    variant_id: UUID | None = None
    branch_id: UUID | None = None
    imei: str | None = None
    purchase_invoice_item_id: UUID | None = None
    sales_invoice_item_id: UUID | None = None
    status: ImeiStatus | None = None
    warranty_expires_at: datetime | None = None


class IMEIItemRead(APIModel):
    id: UUID
    product_id: UUID
    variant_id: UUID | None = None
    branch_id: UUID | None = None
    imei: str
    purchase_invoice_item_id: UUID | None = None
    sales_invoice_item_id: UUID | None = None
    status: ImeiStatus
    warranty_expires_at: datetime | None = None
