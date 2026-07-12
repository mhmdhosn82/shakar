from app.schemas.product import CategoryCreate, CategoryRead, CategoryUpdate
from app.services.product import category_service
from app.utils.helpers import build_crud_router

router = build_crud_router(service=category_service, create_schema=CategoryCreate, update_schema=CategoryUpdate, read_schema=CategoryRead, resource="categories")
