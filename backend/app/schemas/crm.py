from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.schemas.common import APIModel


class CustomerCreate(BaseModel):
    code: str
    full_name: str
    phone: str | None = None
    email: str | None = None
    national_id: str | None = None
    address: str | None = None
    city: str | None = None
    customer_group: str | None = None
    credit_limit: Decimal = Decimal("0")
    total_debt: Decimal = Decimal("0")
    loyalty_points: int = 0
    branch_id: UUID | None = None
    notes: str | None = None


class CustomerUpdate(BaseModel):
    code: str | None = None
    full_name: str | None = None
    phone: str | None = None
    email: str | None = None
    national_id: str | None = None
    address: str | None = None
    city: str | None = None
    customer_group: str | None = None
    credit_limit: Decimal | None = None
    total_debt: Decimal | None = None
    loyalty_points: int | None = None
    branch_id: UUID | None = None
    notes: str | None = None


class CustomerRead(APIModel):
    id: UUID
    code: str
    full_name: str
    phone: str | None = None
    email: str | None = None
    national_id: str | None = None
    address: str | None = None
    city: str | None = None
    customer_group: str | None = None
    credit_limit: Decimal
    total_debt: Decimal
    loyalty_points: int
    branch_id: UUID | None = None
    notes: str | None = None


class SupplierCreate(BaseModel):
    code: str
    company_name: str
    contact_person: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    city: str | None = None
    tax_id: str | None = None
    total_debt: Decimal = Decimal("0")
    branch_id: UUID | None = None
    notes: str | None = None


class SupplierUpdate(BaseModel):
    code: str | None = None
    company_name: str | None = None
    contact_person: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    city: str | None = None
    tax_id: str | None = None
    total_debt: Decimal | None = None
    branch_id: UUID | None = None
    notes: str | None = None


class SupplierRead(APIModel):
    id: UUID
    code: str
    company_name: str
    contact_person: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    city: str | None = None
    tax_id: str | None = None
    total_debt: Decimal
    branch_id: UUID | None = None
    notes: str | None = None
