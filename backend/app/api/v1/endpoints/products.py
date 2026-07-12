from fastapi import APIRouter

from app.schemas.product import (
    IMEIItemCreate,
    IMEIItemRead,
    IMEIItemUpdate,
    ProductCreate,
    ProductRead,
    ProductUpdate,
    ProductVariantCreate,
    ProductVariantRead,
    ProductVariantUpdate,
)
from app.services.product import imei_item_service, product_service, product_variant_service
from app.utils.helpers import build_crud_router

router = APIRouter()
router.include_router(build_crud_router(service=product_service, create_schema=ProductCreate, update_schema=ProductUpdate, read_schema=ProductRead, resource="products"))
router.include_router(
    build_crud_router(
        service=product_variant_service,
        create_schema=ProductVariantCreate,
        update_schema=ProductVariantUpdate,
        read_schema=ProductVariantRead,
        resource="products",
    ),
    prefix="/variants",
)
router.include_router(
    build_crud_router(service=imei_item_service, create_schema=IMEIItemCreate, update_schema=IMEIItemUpdate, read_schema=IMEIItemRead, resource="products"),
    prefix="/imei-items",
)
