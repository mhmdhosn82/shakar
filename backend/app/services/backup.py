from __future__ import annotations

from datetime import datetime, timezone

from app.core.config import get_settings


class BackupService:
    async def get_strategy(self) -> dict:
        settings = get_settings()
        return {
            "database_url": settings.DATABASE_URL,
            "strategy": "Use pg_dump with custom format for PostgreSQL backups.",
            "command_template": "pg_dump --format=custom --no-owner --dbname=$DATABASE_URL --file=backups/<timestamp>.dump",
            "restore_template": "pg_restore --clean --if-exists --dbname=$DATABASE_URL <backup_file>",
            "notes": [
                "Run backups from a trusted worker with DATABASE_URL injected at runtime.",
                "Store dumps in encrypted object storage with retention policies.",
                "Schedule periodic restore drills to verify backup integrity.",
            ],
        }

    async def create_backup_plan(self, label: str | None = None) -> dict:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        safe_label = (label or "manual").replace(" ", "_")
        return {
            "status": "planned",
            "label": safe_label,
            "filename": f"{timestamp}_{safe_label}.dump",
            "strategy": await self.get_strategy(),
        }


backup_service = BackupService()
