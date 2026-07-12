from app.schemas.product import BrandCreate, BrandRead, BrandUpdate
from app.services.product import brand_service
from app.utils.helpers import build_crud_router

router = build_crud_router(service=brand_service, create_schema=BrandCreate, update_schema=BrandUpdate, read_schema=BrandRead, resource="brands")
