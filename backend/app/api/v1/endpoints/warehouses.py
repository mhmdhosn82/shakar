from app.schemas.warehouse import WarehouseCreate, WarehouseRead, WarehouseUpdate
from app.services.warehouse import warehouse_service
from app.utils.helpers import build_crud_router

router = build_crud_router(service=warehouse_service, create_schema=WarehouseCreate, update_schema=WarehouseUpdate, read_schema=WarehouseRead, resource="warehouses")
