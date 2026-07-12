from fastapi import APIRouter

from app.schemas.accounting import (
    AccountCreate,
    AccountRead,
    AccountUpdate,
    JournalEntryCreate,
    JournalEntryLineCreate,
    JournalEntryLineRead,
    JournalEntryLineUpdate,
    JournalEntryRead,
    JournalEntryUpdate,
)
from app.services.accounting import account_service, journal_entry_line_service, journal_entry_service
from app.utils.helpers import build_crud_router

router = APIRouter()
router.include_router(build_crud_router(service=account_service, create_schema=AccountCreate, update_schema=AccountUpdate, read_schema=AccountRead, resource="accounting"), prefix="/accounts")
router.include_router(build_crud_router(service=journal_entry_service, create_schema=JournalEntryCreate, update_schema=JournalEntryUpdate, read_schema=JournalEntryRead, resource="accounting"), prefix="/journal-entries")
router.include_router(build_crud_router(service=journal_entry_line_service, create_schema=JournalEntryLineCreate, update_schema=JournalEntryLineUpdate, read_schema=JournalEntryLineRead, resource="accounting"), prefix="/journal-entry-lines")
