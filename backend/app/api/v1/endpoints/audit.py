from app.schemas.audit import AuditLogCreate, AuditLogRead, AuditLogUpdate
from app.services.audit import audit_log_service
from app.utils.helpers import build_crud_router

router = build_crud_router(service=audit_log_service, create_schema=AuditLogCreate, update_schema=AuditLogUpdate, read_schema=AuditLogRead, resource="audit")
