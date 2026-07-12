from app.models.purchase import PurchaseInvoice, PurchaseInvoiceItem
from app.utils.helpers import CRUDService

purchase_invoice_service = CRUDService(PurchaseInvoice, search_fields=("invoice_number", "notes"))
purchase_invoice_item_service = CRUDService(PurchaseInvoiceItem)
