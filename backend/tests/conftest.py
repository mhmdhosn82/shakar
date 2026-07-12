from __future__ import annotations

import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def client() -> TestClient:
    db_path = Path(__file__).resolve().parents[1] / "test.db"
    if db_path.exists():
        db_path.unlink()

    os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{db_path.resolve().as_posix()}"
    os.environ["SECRET_KEY"] = "test-secret-key"
    os.environ["BACKEND_CORS_ORIGINS"] = "[]"
    os.environ["FIRST_SUPERUSER_EMAIL"] = "admin@shakar.ir"
    os.environ["FIRST_SUPERUSER_PASSWORD"] = "Admin@123456"

    from app.core.config import get_settings

    get_settings.cache_clear()

    from main import app

    with TestClient(app) as test_client:
        yield test_client

    if db_path.exists():
        db_path.unlink()
