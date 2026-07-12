from __future__ import annotations

from importlib import import_module


def test_app_main_exports_application() -> None:
    root_main = import_module("main")
    package_main = import_module("app.main")

    assert package_main.app is root_main.app
