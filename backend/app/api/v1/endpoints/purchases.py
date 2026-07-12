from fastapi import APIRouter

from app.schemas.purchase import (
    PurchaseInvoiceCreate,
    PurchaseInvoiceItemCreate,
    PurchaseInvoiceItemRead,
    PurchaseInvoiceItemUpdate,
    PurchaseInvoiceRead,
    PurchaseInvoiceUpdate,
)
from app.services.purchase import purchase_invoice_item_service, purchase_invoice_service
from app.utils.helpers import build_crud_router

router = APIRouter()
router.include_router(
    build_crud_router(
        service=purchase_invoice_service,
        create_schema=PurchaseInvoiceCreate,
        update_schema=PurchaseInvoiceUpdate,
        read_schema=PurchaseInvoiceRead,
        resource="purchases",
    )
)
router.include_router(
    build_crud_router(
        service=purchase_invoice_item_service,
        create_schema=PurchaseInvoiceItemCreate,
        update_schema=PurchaseInvoiceItemUpdate,
        read_schema=PurchaseInvoiceItemRead,
        resource="purchases",
    ),
    prefix="/items",
)
