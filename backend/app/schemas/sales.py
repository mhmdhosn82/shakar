from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.models.sales import InstallmentStatus, InvoiceType, PaymentMethod, PaymentType, SalesInvoiceStatus
from app.schemas.common import APIModel


class SalesInvoiceCreate(BaseModel):
    invoice_number: str
    branch_id: UUID
    customer_id: UUID | None = None
    salesperson_id: UUID | None = None
    status: SalesInvoiceStatus = SalesInvoiceStatus.draft
    subtotal: Decimal = Decimal("0")
    discount_amount: Decimal = Decimal("0")
    tax_amount: Decimal = Decimal("0")
    total: Decimal = Decimal("0")
    paid_amount: Decimal = Decimal("0")
    due_amount: Decimal = Decimal("0")
    payment_type: PaymentType = PaymentType.cash
    notes: str | None = None
    issued_at: datetime | None = None


class SalesInvoiceUpdate(BaseModel):
    invoice_number: str | None = None
    branch_id: UUID | None = None
    customer_id: UUID | None = None
    salesperson_id: UUID | None = None
    status: SalesInvoiceStatus | None = None
    subtotal: Decimal | None = None
    discount_amount: Decimal | None = None
    tax_amount: Decimal | None = None
    total: Decimal | None = None
    paid_amount: Decimal | None = None
    due_amount: Decimal | None = None
    payment_type: PaymentType | None = None
    notes: str | None = None
    issued_at: datetime | None = None


class SalesInvoiceRead(APIModel):
    id: UUID
    invoice_number: str
    branch_id: UUID
    customer_id: UUID | None = None
    salesperson_id: UUID | None = None
    status: SalesInvoiceStatus
    subtotal: Decimal
    discount_amount: Decimal
    tax_amount: Decimal
    total: Decimal
    paid_amount: Decimal
    due_amount: Decimal
    payment_type: PaymentType
    notes: str | None = None
    issued_at: datetime


class SalesInvoiceItemCreate(BaseModel):
    invoice_id: UUID
    product_id: UUID
    variant_id: UUID | None = None
    imei_item_id: UUID | None = None
    quantity: int = 1
    unit_price: Decimal = Decimal("0")
    discount_percent: Decimal = Decimal("0")
    line_total: Decimal = Decimal("0")


class SalesInvoiceItemUpdate(BaseModel):
    invoice_id: UUID | None = None
    product_id: UUID | None = None
    variant_id: UUID | None = None
    imei_item_id: UUID | None = None
    quantity: int | None = None
    unit_price: Decimal | None = None
    discount_percent: Decimal | None = None
    line_total: Decimal | None = None


class SalesInvoiceItemRead(APIModel):
    id: UUID
    invoice_id: UUID
    product_id: UUID
    variant_id: UUID | None = None
    imei_item_id: UUID | None = None
    quantity: int
    unit_price: Decimal
    discount_percent: Decimal
    line_total: Decimal


class PaymentCreate(BaseModel):
    invoice_id: UUID
    invoice_type: InvoiceType
    amount: Decimal
    payment_method: PaymentMethod = PaymentMethod.cash
    reference_number: str | None = None
    notes: str | None = None
    paid_at: datetime | None = None
    received_by: UUID | None = None
    branch_id: UUID | None = None


class PaymentUpdate(BaseModel):
    invoice_id: UUID | None = None
    invoice_type: InvoiceType | None = None
    amount: Decimal | None = None
    payment_method: PaymentMethod | None = None
    reference_number: str | None = None
    notes: str | None = None
    paid_at: datetime | None = None
    received_by: UUID | None = None
    branch_id: UUID | None = None


class PaymentRead(APIModel):
    id: UUID
    invoice_id: UUID
    invoice_type: InvoiceType
    amount: Decimal
    payment_method: PaymentMethod
    reference_number: str | None = None
    notes: str | None = None
    paid_at: datetime
    received_by: UUID | None = None
    branch_id: UUID | None = None


class InstallmentPlanCreate(BaseModel):
    invoice_id: UUID
    down_payment: Decimal = Decimal("0")
    total_installments: int = 1
    installment_amount: Decimal = Decimal("0")
    interest_rate: Decimal = Decimal("0")
    notes: str | None = None


class InstallmentPlanUpdate(BaseModel):
    invoice_id: UUID | None = None
    down_payment: Decimal | None = None
    total_installments: int | None = None
    installment_amount: Decimal | None = None
    interest_rate: Decimal | None = None
    notes: str | None = None


class InstallmentPlanRead(APIModel):
    id: UUID
    invoice_id: UUID
    down_payment: Decimal
    total_installments: int
    installment_amount: Decimal
    interest_rate: Decimal
    notes: str | None = None


class InstallmentScheduleCreate(BaseModel):
    plan_id: UUID
    due_date: datetime
    amount: Decimal
    paid_amount: Decimal = Decimal("0")
    status: InstallmentStatus = InstallmentStatus.pending
    paid_at: datetime | None = None


class InstallmentScheduleUpdate(BaseModel):
    plan_id: UUID | None = None
    due_date: datetime | None = None
    amount: Decimal | None = None
    paid_amount: Decimal | None = None
    status: InstallmentStatus | None = None
    paid_at: datetime | None = None


class InstallmentScheduleRead(APIModel):
    id: UUID
    plan_id: UUID
    due_date: datetime
    amount: Decimal
    paid_amount: Decimal
    status: InstallmentStatus
    paid_at: datetime | None = None
