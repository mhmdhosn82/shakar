from __future__ import annotations

import enum
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Numeric, String, Text, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import TimestampedUUIDModel, utcnow


class AccountType(str, enum.Enum):
    asset = "asset"
    liability = "liability"
    equity = "equity"
    income = "income"
    expense = "expense"


class JournalEntryStatus(str, enum.Enum):
    draft = "draft"
    posted = "posted"
    reversed = "reversed"


class Account(TimestampedUUIDModel):
    __tablename__ = "accounts"

    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    account_type: Mapped[AccountType] = mapped_column(Enum(AccountType), nullable=False)
    parent_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("accounts.id"), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=text("true"), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    parent: Mapped[Account | None] = relationship(remote_side="Account.id", back_populates="children")
    children: Mapped[list[Account]] = relationship(back_populates="parent")
    journal_lines: Mapped[list["JournalEntryLine"]] = relationship(back_populates="account")

    def __repr__(self) -> str:
        return f"<Account(code={self.code!r}, name={self.name!r})>"


class JournalEntry(TimestampedUUIDModel):
    __tablename__ = "journal_entries"

    entry_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    branch_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("branches.id"), nullable=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    entry_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    status: Mapped[JournalEntryStatus] = mapped_column(Enum(JournalEntryStatus), default=JournalEntryStatus.draft, nullable=False)
    created_by: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("users.id"), nullable=True)
    total_debit: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    total_credit: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)

    branch: Mapped["Branch"] = relationship()
    creator: Mapped["User"] = relationship()
    lines: Mapped[list["JournalEntryLine"]] = relationship(back_populates="entry", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<JournalEntry(entry_number={self.entry_number!r}, status={self.status.value!r})>"


class JournalEntryLine(TimestampedUUIDModel):
    __tablename__ = "journal_entry_lines"

    entry_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("journal_entries.id", ondelete="CASCADE"), nullable=False, index=True)
    account_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("accounts.id"), nullable=False, index=True)
    debit: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    credit: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    reference_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, nullable=True)
    reference_type: Mapped[str | None] = mapped_column(String(100), nullable=True)

    entry: Mapped[JournalEntry] = relationship(back_populates="lines")
    account: Mapped[Account] = relationship(back_populates="journal_lines")

    def __repr__(self) -> str:
        return f"<JournalEntryLine(entry_id={self.entry_id}, account_id={self.account_id})>"


