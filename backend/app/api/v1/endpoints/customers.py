from app.schemas.crm import CustomerCreate, CustomerRead, CustomerUpdate
from app.services.crm import customer_service
from app.utils.helpers import build_crud_router

router = build_crud_router(service=customer_service, create_schema=CustomerCreate, update_schema=CustomerUpdate, read_schema=CustomerRead, resource="customers")
