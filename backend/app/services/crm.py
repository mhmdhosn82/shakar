from app.models.crm import Customer, Supplier
from app.utils.helpers import CRUDService

customer_service = CRUDService(Customer, search_fields=("code", "full_name", "phone", "email"))
supplier_service = CRUDService(Supplier, search_fields=("code", "company_name", "contact_person", "phone"))
