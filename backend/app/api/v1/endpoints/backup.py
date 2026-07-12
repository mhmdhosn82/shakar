from __future__ import annotations

from pydantic import BaseModel
from fastapi import APIRouter, Depends, status

from app.core.deps import get_current_active_user, require_permission
from app.models.user import User
from app.services.backup import backup_service

router = APIRouter()


class BackupRequest(BaseModel):
    label: str | None = None


@router.get("/strategy", dependencies=[Depends(require_permission("backup", "read"))])
async def get_backup_strategy(_: User = Depends(get_current_active_user)) -> dict:
    return await backup_service.get_strategy()


@router.post("/run", status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(require_permission("backup", "create"))])
async def plan_backup(payload: BackupRequest, _: User = Depends(get_current_active_user)) -> dict:
    return await backup_service.create_backup_plan(payload.label)
