from app.schemas.branch import BranchCreate, BranchRead, BranchUpdate
from app.services.branch import branch_service
from app.utils.helpers import build_crud_router

router = build_crud_router(service=branch_service, create_schema=BranchCreate, update_schema=BranchUpdate, read_schema=BranchRead, resource="branches")
