from __future__ import annotations

import enum
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, Text, Uuid
from sqlalchemy.orm import Mapped, foreign, mapped_column, relationship

from app.models.base import TimestampedUUIDModel, utcnow


class PurchaseInvoiceStatus(str, enum.Enum):
    draft = "draft"
    confirmed = "confirmed"
    received = "received"
    cancelled = "cancelled"


class PurchaseInvoice(TimestampedUUIDModel):
    __tablename__ = "purchase_invoices"

    invoice_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    branch_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("branches.id"), nullable=False, index=True)
    supplier_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("suppliers.id"), nullable=True, index=True)
    warehouse_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("warehouses.id"), nullable=True, index=True)
    status: Mapped[PurchaseInvoiceStatus] = mapped_column(Enum(PurchaseInvoiceStatus), default=PurchaseInvoiceStatus.draft, nullable=False)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    discount_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    extra_costs: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    total: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    paid_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    due_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    branch: Mapped["Branch"] = relationship()
    supplier: Mapped["Supplier"] = relationship()
    warehouse: Mapped["Warehouse"] = relationship(back_populates="purchase_invoices")
    items: Mapped[list["PurchaseInvoiceItem"]] = relationship(back_populates="invoice", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<PurchaseInvoice(invoice_number={self.invoice_number!r}, total={self.total})>"


class PurchaseInvoiceItem(TimestampedUUIDModel):
    __tablename__ = "purchase_invoice_items"

    invoice_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("purchase_invoices.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("products.id"), nullable=False, index=True)
    variant_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("product_variants.id"), nullable=True, index=True)
    quantity: Mapped[int] = mapped_column(default=1, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    line_total: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)

    invoice: Mapped[PurchaseInvoice] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship()
    variant: Mapped["ProductVariant"] = relationship()
    imei_items: Mapped[list["IMEIItem"]] = relationship(
        primaryjoin="PurchaseInvoiceItem.id == foreign(IMEIItem.purchase_invoice_item_id)",
        viewonly=True,
    )

    def __repr__(self) -> str:
        return f"<PurchaseInvoiceItem(invoice_id={self.invoice_id}, quantity={self.quantity})>"


