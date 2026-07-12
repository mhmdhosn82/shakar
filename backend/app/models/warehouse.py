from __future__ import annotations

import enum
import uuid

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, Numeric, String, Text, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BranchScopedMixin, TimestampedUUIDModel


class StockMovementType(str, enum.Enum):
    purchase = "purchase"
    sale = "sale"
    transfer = "transfer"
    adjustment = "adjustment"
    return_ = "return"


class Warehouse(TimestampedUUIDModel):
    __tablename__ = "warehouses"

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    branch_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("branches.id"), nullable=False, index=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=text("true"), nullable=False)

    branch: Mapped["Branch"] = relationship(back_populates="warehouses")
    stock_items: Mapped[list["Stock"]] = relationship(back_populates="warehouse")
    stock_movements: Mapped[list["StockMovement"]] = relationship(back_populates="warehouse")
    purchase_invoices: Mapped[list["PurchaseInvoice"]] = relationship(back_populates="warehouse")

    def __repr__(self) -> str:
        return f"<Warehouse(code={self.code!r}, name={self.name!r})>"


class Stock(TimestampedUUIDModel, BranchScopedMixin):
    __tablename__ = "stock"

    product_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("products.id"), nullable=False, index=True)
    variant_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("product_variants.id"), nullable=True, index=True)
    warehouse_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("warehouses.id"), nullable=False, index=True)
    quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    reserved_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    warehouse: Mapped[Warehouse] = relationship(back_populates="stock_items")
    product: Mapped["Product"] = relationship()
    variant: Mapped["ProductVariant"] = relationship()

    def __repr__(self) -> str:
        return f"<Stock(product_id={self.product_id}, warehouse_id={self.warehouse_id}, quantity={self.quantity})>"


class StockMovement(TimestampedUUIDModel, BranchScopedMixin):
    __tablename__ = "stock_movements"

    product_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("products.id"), nullable=False, index=True)
    variant_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("product_variants.id"), nullable=True, index=True)
    warehouse_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("warehouses.id"), nullable=False, index=True)
    movement_type: Mapped[StockMovementType] = mapped_column(Enum(StockMovementType), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    reference_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, nullable=True)
    reference_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("users.id"), nullable=True)

    warehouse: Mapped[Warehouse] = relationship(back_populates="stock_movements")
    product: Mapped["Product"] = relationship()
    variant: Mapped["ProductVariant"] = relationship()
    created_by_user: Mapped["User"] = relationship()

    def __repr__(self) -> str:
        return f"<StockMovement(type={self.movement_type.value!r}, quantity={self.quantity})>"


