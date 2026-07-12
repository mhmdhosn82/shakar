from fastapi import APIRouter

from app.schemas.user import (
    PermissionCreate,
    PermissionRead,
    PermissionUpdate,
    RoleCreate,
    RoleRead,
    RoleUpdate,
    UserCreate,
    UserRead,
    UserUpdate,
)
from app.services.user import permission_service, role_service, user_service
from app.utils.helpers import build_crud_router

router = APIRouter()
router.include_router(build_crud_router(service=user_service, create_schema=UserCreate, update_schema=UserUpdate, read_schema=UserRead, resource="users"))
router.include_router(
    build_crud_router(service=role_service, create_schema=RoleCreate, update_schema=RoleUpdate, read_schema=RoleRead, resource="roles"),
    prefix="/roles",
)
router.include_router(
    build_crud_router(
        service=permission_service,
        create_schema=PermissionCreate,
        update_schema=PermissionUpdate,
        read_schema=PermissionRead,
        resource="permissions",
    ),
    prefix="/permissions",
)
