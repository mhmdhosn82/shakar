from __future__ import annotations

import enum
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Enum, ForeignKey, JSON, Numeric, String, Text, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BranchScopedMixin, TimestampedUUIDModel


class ProductType(str, enum.Enum):
    accessory = "accessory"
    mobile = "mobile"
    other = "other"


class ImeiStatus(str, enum.Enum):
    in_stock = "in_stock"
    sold = "sold"
    reserved = "reserved"
    returned = "returned"


class Category(TimestampedUUIDModel):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    parent_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("categories.id"), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    parent: Mapped[Category | None] = relationship(remote_side="Category.id", back_populates="children")
    children: Mapped[list[Category]] = relationship(back_populates="parent")
    products: Mapped[list["Product"]] = relationship(back_populates="category")

    def __repr__(self) -> str:
        return f"<Category(code={self.code!r}, name={self.name!r})>"


class Brand(TimestampedUUIDModel):
    __tablename__ = "brands"

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    country_of_origin: Mapped[str | None] = mapped_column(String(100), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    products: Mapped[list["Product"]] = relationship(back_populates="brand")

    def __repr__(self) -> str:
        return f"<Brand(code={self.code!r}, name={self.name!r})>"


class Product(TimestampedUUIDModel, BranchScopedMixin):
    __tablename__ = "products"

    sku: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    barcode: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("categories.id"), nullable=True)
    brand_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("brands.id"), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    product_type: Mapped[ProductType] = mapped_column(Enum(ProductType), default=ProductType.other, nullable=False)
    unit: Mapped[str] = mapped_column(String(50), default="piece", nullable=False)
    min_stock_alert: Mapped[int] = mapped_column(default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, server_default=text("true"), nullable=False)

    category: Mapped[Category | None] = relationship(back_populates="products")
    brand: Mapped[Brand | None] = relationship(back_populates="products")
    variants: Mapped[list["ProductVariant"]] = relationship(back_populates="product", cascade="all, delete-orphan")
    imei_items: Mapped[list["IMEIItem"]] = relationship(back_populates="product")

    def __repr__(self) -> str:
        return f"<Product(sku={self.sku!r}, name={self.name!r})>"


class ProductVariant(TimestampedUUIDModel):
    __tablename__ = "product_variants"

    product_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    color: Mapped[str | None] = mapped_column(String(80), nullable=True)
    storage_capacity: Mapped[str | None] = mapped_column(String(50), nullable=True)
    ram: Mapped[str | None] = mapped_column(String(50), nullable=True)
    attributes: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    sku_suffix: Mapped[str | None] = mapped_column(String(50), nullable=True)
    extra_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)

    product: Mapped[Product] = relationship(back_populates="variants")
    imei_items: Mapped[list["IMEIItem"]] = relationship(back_populates="variant")

    def __repr__(self) -> str:
        return f"<ProductVariant(product_id={self.product_id}, sku_suffix={self.sku_suffix!r})>"


class IMEIItem(TimestampedUUIDModel, BranchScopedMixin):
    __tablename__ = "imei_items"

    product_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("products.id"), nullable=False, index=True)
    variant_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("product_variants.id"), nullable=True, index=True)
    imei: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    purchase_invoice_item_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("purchase_invoice_items.id"), nullable=True)
    sales_invoice_item_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("sales_invoice_items.id"), nullable=True)
    status: Mapped[ImeiStatus] = mapped_column(Enum(ImeiStatus), default=ImeiStatus.in_stock, nullable=False)
    warranty_expires_at: Mapped[datetime | None] = mapped_column(nullable=True)

    product: Mapped[Product] = relationship(back_populates="imei_items")
    variant: Mapped[ProductVariant | None] = relationship(back_populates="imei_items")

    def __repr__(self) -> str:
        return f"<IMEIItem(imei={self.imei!r}, status={self.status.value!r})>"
