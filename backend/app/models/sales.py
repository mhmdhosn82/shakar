from __future__ import annotations

import enum
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import TimestampedUUIDModel, utcnow


class SalesInvoiceStatus(str, enum.Enum):
    draft = "draft"
    confirmed = "confirmed"
    cancelled = "cancelled"


class PaymentType(str, enum.Enum):
    cash = "cash"
    installment = "installment"
    credit = "credit"


class InvoiceType(str, enum.Enum):
    sales = "sales"
    purchase = "purchase"


class PaymentMethod(str, enum.Enum):
    cash = "cash"
    card = "card"
    bank_transfer = "bank_transfer"
    check = "check"


class InstallmentStatus(str, enum.Enum):
    pending = "pending"
    paid = "paid"
    overdue = "overdue"


class SalesInvoice(TimestampedUUIDModel):
    __tablename__ = "sales_invoices"

    invoice_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    branch_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("branches.id"), nullable=False, index=True)
    customer_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("customers.id"), nullable=True, index=True)
    salesperson_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("users.id"), nullable=True, index=True)
    status: Mapped[SalesInvoiceStatus] = mapped_column(Enum(SalesInvoiceStatus), default=SalesInvoiceStatus.draft, nullable=False)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    discount_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    total: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    paid_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    due_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    payment_type: Mapped[PaymentType] = mapped_column(Enum(PaymentType), default=PaymentType.cash, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    branch: Mapped["Branch"] = relationship()
    customer: Mapped["Customer"] = relationship()
    salesperson: Mapped["User"] = relationship()
    items: Mapped[list["SalesInvoiceItem"]] = relationship(back_populates="invoice", cascade="all, delete-orphan")
    installment_plans: Mapped[list["InstallmentPlan"]] = relationship(back_populates="invoice", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<SalesInvoice(invoice_number={self.invoice_number!r}, total={self.total})>"


class SalesInvoiceItem(TimestampedUUIDModel):
    __tablename__ = "sales_invoice_items"

    invoice_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("sales_invoices.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("products.id"), nullable=False, index=True)
    variant_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("product_variants.id"), nullable=True, index=True)
    imei_item_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("imei_items.id"), nullable=True, index=True)
    quantity: Mapped[int] = mapped_column(default=1, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    discount_percent: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=0, nullable=False)
    line_total: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)

    invoice: Mapped[SalesInvoice] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship()
    variant: Mapped["ProductVariant"] = relationship()
    imei_item: Mapped["IMEIItem"] = relationship(foreign_keys=[imei_item_id])

    def __repr__(self) -> str:
        return f"<SalesInvoiceItem(invoice_id={self.invoice_id}, quantity={self.quantity})>"


class Payment(TimestampedUUIDModel):
    __tablename__ = "payments"

    invoice_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False, index=True)
    invoice_type: Mapped[InvoiceType] = mapped_column(Enum(InvoiceType), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    payment_method: Mapped[PaymentMethod] = mapped_column(Enum(PaymentMethod), default=PaymentMethod.cash, nullable=False)
    reference_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    paid_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    received_by: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("users.id"), nullable=True)
    branch_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("branches.id"), nullable=True, index=True)

    receiver: Mapped["User"] = relationship()
    branch: Mapped["Branch"] = relationship()

    def __repr__(self) -> str:
        return f"<Payment(invoice_id={self.invoice_id}, amount={self.amount})>"


class InstallmentPlan(TimestampedUUIDModel):
    __tablename__ = "installment_plans"

    invoice_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("sales_invoices.id", ondelete="CASCADE"), nullable=False, index=True)
    down_payment: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    total_installments: Mapped[int] = mapped_column(default=1, nullable=False)
    installment_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    interest_rate: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=0, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    invoice: Mapped[SalesInvoice] = relationship(back_populates="installment_plans")
    schedules: Mapped[list["InstallmentSchedule"]] = relationship(back_populates="plan", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<InstallmentPlan(invoice_id={self.invoice_id}, total_installments={self.total_installments})>"


class InstallmentSchedule(TimestampedUUIDModel):
    __tablename__ = "installment_schedules"

    plan_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("installment_plans.id", ondelete="CASCADE"), nullable=False, index=True)
    due_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    paid_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    status: Mapped[InstallmentStatus] = mapped_column(Enum(InstallmentStatus), default=InstallmentStatus.pending, nullable=False)
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    plan: Mapped[InstallmentPlan] = relationship(back_populates="schedules")

    def __repr__(self) -> str:
        return f"<InstallmentSchedule(plan_id={self.plan_id}, due_date={self.due_date})>"


