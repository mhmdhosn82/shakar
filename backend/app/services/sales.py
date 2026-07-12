from app.models.sales import InstallmentPlan, InstallmentSchedule, Payment, SalesInvoice, SalesInvoiceItem
from app.utils.helpers import CRUDService

sales_invoice_service = CRUDService(SalesInvoice, search_fields=("invoice_number", "notes"))
sales_invoice_item_service = CRUDService(SalesInvoiceItem)
payment_service = CRUDService(Payment, search_fields=("reference_number", "notes"))
installment_plan_service = CRUDService(InstallmentPlan, search_fields=("notes",))
installment_schedule_service = CRUDService(InstallmentSchedule)
