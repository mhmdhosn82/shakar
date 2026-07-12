from fastapi import APIRouter

from app.schemas.warehouse import (
    StockCreate,
    StockMovementCreate,
    StockMovementRead,
    StockMovementUpdate,
    StockRead,
    StockUpdate,
)
from app.services.warehouse import stock_movement_service, stock_service
from app.utils.helpers import build_crud_router

router = APIRouter()
router.include_router(build_crud_router(service=stock_service, create_schema=StockCreate, update_schema=StockUpdate, read_schema=StockRead, resource="inventory"))
router.include_router(
    build_crud_router(
        service=stock_movement_service,
        create_schema=StockMovementCreate,
        update_schema=StockMovementUpdate,
        read_schema=StockMovementRead,
        resource="inventory",
    ),
    prefix="/movements",
)
