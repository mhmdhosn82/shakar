from app.models.accounting import Account, JournalEntry, JournalEntryLine
from app.utils.helpers import CRUDService

account_service = CRUDService(Account, search_fields=("code", "name", "description"))
journal_entry_service = CRUDService(JournalEntry, search_fields=("entry_number", "description"))
journal_entry_line_service = CRUDService(JournalEntryLine, search_fields=("description", "reference_type"))
