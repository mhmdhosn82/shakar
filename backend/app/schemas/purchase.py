from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.models.purchase import PurchaseInvoiceStatus
from app.schemas.common import APIModel


class PurchaseInvoiceCreate(BaseModel):
    invoice_number: str
    branch_id: UUID
    supplier_id: UUID | None = None
    warehouse_id: UUID | None = None
    status: PurchaseInvoiceStatus = PurchaseInvoiceStatus.draft
    subtotal: Decimal = Decimal("0")
    discount_amount: Decimal = Decimal("0")
    tax_amount: Decimal = Decimal("0")
    extra_costs: Decimal = Decimal("0")
    total: Decimal = Decimal("0")
    paid_amount: Decimal = Decimal("0")
    due_amount: Decimal = Decimal("0")
    notes: str | None = None
    issued_at: datetime | None = None


class PurchaseInvoiceUpdate(BaseModel):
    invoice_number: str | None = None
    branch_id: UUID | None = None
    supplier_id: UUID | None = None
    warehouse_id: UUID | None = None
    status: PurchaseInvoiceStatus | None = None
    subtotal: Decimal | None = None
    discount_amount: Decimal | None = None
    tax_amount: Decimal | None = None
    extra_costs: Decimal | None = None
    total: Decimal | None = None
    paid_amount: Decimal | None = None
    due_amount: Decimal | None = None
    notes: str | None = None
    issued_at: datetime | None = None


class PurchaseInvoiceRead(APIModel):
    id: UUID
    invoice_number: str
    branch_id: UUID
    supplier_id: UUID | None = None
    warehouse_id: UUID | None = None
    status: PurchaseInvoiceStatus
    subtotal: Decimal
    discount_amount: Decimal
    tax_amount: Decimal
    extra_costs: Decimal
    total: Decimal
    paid_amount: Decimal
    due_amount: Decimal
    notes: str | None = None
    issued_at: datetime


class PurchaseInvoiceItemCreate(BaseModel):
    invoice_id: UUID
    product_id: UUID
    variant_id: UUID | None = None
    quantity: int = 1
    unit_price: Decimal = Decimal("0")
    line_total: Decimal = Decimal("0")


class PurchaseInvoiceItemUpdate(BaseModel):
    invoice_id: UUID | None = None
    product_id: UUID | None = None
    variant_id: UUID | None = None
    quantity: int | None = None
    unit_price: Decimal | None = None
    line_total: Decimal | None = None


class PurchaseInvoiceItemRead(APIModel):
    id: UUID
    invoice_id: UUID
    product_id: UUID
    variant_id: UUID | None = None
    quantity: int
    unit_price: Decimal
    line_total: Decimal
