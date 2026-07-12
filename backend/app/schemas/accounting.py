from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.models.accounting import AccountType, JournalEntryStatus
from app.schemas.common import APIModel


class AccountCreate(BaseModel):
    code: str
    name: str
    account_type: AccountType
    parent_id: UUID | None = None
    is_active: bool = True
    description: str | None = None


class AccountUpdate(BaseModel):
    code: str | None = None
    name: str | None = None
    account_type: AccountType | None = None
    parent_id: UUID | None = None
    is_active: bool | None = None
    description: str | None = None


class AccountRead(APIModel):
    id: UUID
    code: str
    name: str
    account_type: AccountType
    parent_id: UUID | None = None
    is_active: bool
    description: str | None = None


class JournalEntryCreate(BaseModel):
    entry_number: str
    branch_id: UUID | None = None
    description: str | None = None
    entry_date: datetime | None = None
    status: JournalEntryStatus = JournalEntryStatus.draft
    created_by: UUID | None = None
    total_debit: Decimal = Decimal("0")
    total_credit: Decimal = Decimal("0")


class JournalEntryUpdate(BaseModel):
    entry_number: str | None = None
    branch_id: UUID | None = None
    description: str | None = None
    entry_date: datetime | None = None
    status: JournalEntryStatus | None = None
    created_by: UUID | None = None
    total_debit: Decimal | None = None
    total_credit: Decimal | None = None


class JournalEntryRead(APIModel):
    id: UUID
    entry_number: str
    branch_id: UUID | None = None
    description: str | None = None
    entry_date: datetime
    status: JournalEntryStatus
    created_by: UUID | None = None
    total_debit: Decimal
    total_credit: Decimal


class JournalEntryLineCreate(BaseModel):
    entry_id: UUID
    account_id: UUID
    debit: Decimal = Decimal("0")
    credit: Decimal = Decimal("0")
    description: str | None = None
    reference_id: UUID | None = None
    reference_type: str | None = None


class JournalEntryLineUpdate(BaseModel):
    entry_id: UUID | None = None
    account_id: UUID | None = None
    debit: Decimal | None = None
    credit: Decimal | None = None
    description: str | None = None
    reference_id: UUID | None = None
    reference_type: str | None = None


class JournalEntryLineRead(APIModel):
    id: UUID
    entry_id: UUID
    account_id: UUID
    debit: Decimal
    credit: Decimal
    description: str | None = None
    reference_id: UUID | None = None
    reference_type: str | None = None
