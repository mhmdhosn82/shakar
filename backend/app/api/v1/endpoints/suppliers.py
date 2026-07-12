from app.schemas.crm import SupplierCreate, SupplierRead, SupplierUpdate
from app.services.crm import supplier_service
from app.utils.helpers import build_crud_router

router = build_crud_router(service=supplier_service, create_schema=SupplierCreate, update_schema=SupplierUpdate, read_schema=SupplierRead, resource="suppliers")
