from __future__ import annotations

import os
import sys

from .config import APP_NAME, APP_VERSION
from .database import initialize_database
from .services import ShakarService


def run() -> int:
    if sys.platform != "win32" and not os.environ.get("DISPLAY"):
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QApplication

    from .ui.theme import APP_STYLE
    from .ui.windows import LoginDialog, MainWindow

    initialize_database()
    service = ShakarService()
    app = QApplication.instance() or QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setLayoutDirection(Qt.RightToLeft)
    app.setStyleSheet(APP_STYLE)

    login = LoginDialog(service)
    if login.exec() != LoginDialog.Accepted or login.user is None:
        return 0

    window = MainWindow(service, login.user)
    window.show()
    return app.exec()
