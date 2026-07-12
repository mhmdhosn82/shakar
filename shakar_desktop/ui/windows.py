from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any, Callable

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QTextDocument
from PySide6.QtPrintSupport import QPrinter
from PySide6.QtWidgets import (
    QButtonGroup,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QDialog,
    QLineEdit,
)

from ..config import APP_NAME, BACKUP_DIR, EXPORT_DIR, WINDOW_MIN_SIZE
from ..services import AuthenticatedUser, ShakarService
from .dialogs import SimpleFormDialog

ACTION_LABELS = {
    "new_customer": "ثبت مشتری",
    "new_user": "کاربر جدید",
    "new_expense": "ثبت هزینه",
    "new_repair": "پذیرش تعمیر",
    "new_sale": "فروش سریع",
    "backup": "بکاپ",
    "restore": "بازیابی",
}


def make_card(label: str, value: str) -> QFrame:
    card = QFrame()
    card.setObjectName("Card")
    layout = QVBoxLayout(card)
    title = QLabel(label)
    title.setObjectName("Subtitle")
    value_label = QLabel(value)
    value_label.setStyleSheet("font-size: 20px; font-weight: 700; color: white;")
    layout.addWidget(title)
    layout.addWidget(value_label)
    return card


class LoginDialog(QDialog):
    def __init__(self, service: ShakarService, parent=None) -> None:
        super().__init__(parent)
        self.service = service
        self.user: AuthenticatedUser | None = None
        self.setWindowTitle(f"ورود به {APP_NAME}")
        self.resize(460, 360)

        layout = QVBoxLayout(self)
        title = QLabel(APP_NAME)
        title.setObjectName("Title")
        layout.addWidget(title)
        subtitle = QLabel("نرم‌افزار حرفه‌ای فروشگاه موبایل و اکسسوری — اجرای ساده با python main.py")
        subtitle.setWordWrap(True)
        subtitle.setObjectName("Subtitle")
        layout.addWidget(subtitle)

        hint = QLabel("ورود دمو: admin / Admin@123456")
        hint.setStyleSheet("color:#93c5fd;")
        layout.addWidget(hint)

        self.username = QLineEdit("admin")
        self.username.setPlaceholderText("نام کاربری یا ایمیل")
        self.password = QLineEdit("Admin@123456")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText("رمز عبور")
        layout.addWidget(self.username)
        layout.addWidget(self.password)

        self.error = QLabel("")
        self.error.setStyleSheet("color:#fca5a5;")
        layout.addWidget(self.error)

        button = QPushButton("ورود")
        button.clicked.connect(self._login)
        layout.addWidget(button)

    def _login(self) -> None:
        user = self.service.authenticate(self.username.text().strip(), self.password.text())
        if user is None:
            self.error.setText("نام کاربری یا رمز عبور نامعتبر است.")
            return
        self.user = user
        self.accept()


class ModulePage(QWidget):
    def __init__(self, service: ShakarService, user: AuthenticatedUser, module_key: str, action_handler: Callable[[str], None], parent=None) -> None:
        super().__init__(parent)
        self.service = service
        self.user = user
        self.module_key = module_key
        self.action_handler = action_handler
        self.payload: dict[str, Any] = {}

        root = QVBoxLayout(self)
        self.header_title = QLabel()
        self.header_title.setObjectName("Title")
        self.header_subtitle = QLabel()
        self.header_subtitle.setWordWrap(True)
        self.header_subtitle.setObjectName("Subtitle")
        root.addWidget(self.header_title)
        root.addWidget(self.header_subtitle)

        toolbar = QHBoxLayout()
        toolbar.addStretch(1)
        self.actions_container = QHBoxLayout()
        toolbar.addLayout(self.actions_container)
        refresh_btn = QPushButton("نوسازی")
        refresh_btn.setProperty("variant", "secondary")
        refresh_btn.clicked.connect(self.refresh)
        toolbar.addWidget(refresh_btn)
        csv_btn = QPushButton("خروجی CSV")
        csv_btn.setProperty("variant", "ghost")
        csv_btn.clicked.connect(self.export_csv)
        toolbar.addWidget(csv_btn)
        pdf_btn = QPushButton("گزارش PDF")
        pdf_btn.setProperty("variant", "ghost")
        pdf_btn.clicked.connect(self.export_pdf)
        toolbar.addWidget(pdf_btn)
        root.addLayout(toolbar)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.content_layout = QVBoxLayout(self.scroll_content)
        self.content_layout.setAlignment(Qt.AlignTop)
        self.scroll.setWidget(self.scroll_content)
        root.addWidget(self.scroll)
        self.refresh()

    def clear_layout(self, layout: QVBoxLayout | QHBoxLayout) -> None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            child_layout = item.layout()
            if widget is not None:
                widget.deleteLater()
            elif child_layout is not None:
                self.clear_layout(child_layout)

    def refresh(self) -> None:
        self.payload = self.service.get_payload(self.module_key, self.user)
        self.header_title.setText(self.payload.get("title", ""))
        self.header_subtitle.setText(self.payload.get("subtitle", ""))
        self.clear_layout(self.actions_container)
        self.clear_layout(self.content_layout)

        for action_code in self.payload.get("actions", []):
            btn = QPushButton(ACTION_LABELS.get(action_code, action_code))
            btn.setProperty("variant", "secondary")
            btn.clicked.connect(lambda checked=False, code=action_code: self.action_handler(code))
            self.actions_container.addWidget(btn)

        cards_layout = QGridLayout()
        for index, card in enumerate(self.payload.get("cards", [])):
            cards_layout.addWidget(make_card(card["label"], card["value"]), index // 3, index % 3)
        self.content_layout.addLayout(cards_layout)

        for table in self.payload.get("tables", []):
            self.content_layout.addWidget(self._table_frame(table))

        if self.payload.get("insights"):
            insight_card = QFrame()
            insight_card.setObjectName("Card")
            layout = QVBoxLayout(insight_card)
            title = QLabel("نکات مدیریتی و هوشمند")
            title.setStyleSheet("font-size:16px; font-weight:700;")
            layout.addWidget(title)
            for line in self.payload["insights"]:
                label = QLabel(f"• {line}")
                label.setWordWrap(True)
                layout.addWidget(label)
            self.content_layout.addWidget(insight_card)
        self.content_layout.addStretch(1)

    def _table_frame(self, table: dict[str, Any]) -> QFrame:
        frame = QFrame()
        frame.setObjectName("Card")
        layout = QVBoxLayout(frame)
        title = QLabel(table.get("title", "جدول"))
        title.setStyleSheet("font-size:16px; font-weight:700;")
        layout.addWidget(title)
        widget = QTableWidget()
        widget.setAlternatingRowColors(True)
        widget.setEditTriggers(QTableWidget.NoEditTriggers)
        widget.setSelectionBehavior(QTableWidget.SelectRows)
        widget.setColumnCount(len(table.get("columns", [])))
        widget.setHorizontalHeaderLabels(table.get("columns", []))
        widget.setRowCount(len(table.get("rows", [])))
        for row_index, row in enumerate(table.get("rows", [])):
            for column_index, value in enumerate(row):
                widget.setItem(row_index, column_index, QTableWidgetItem(value))
        widget.resizeColumnsToContents()
        widget.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(widget)
        return frame

    def export_csv(self) -> None:
        if not self.payload.get("tables"):
            QMessageBox.information(self, "خروجی", "جدولی برای خروجی وجود ندارد.")
            return
        default = EXPORT_DIR / f"{self.module_key}.csv"
        path, _ = QFileDialog.getSaveFileName(self, "ذخیره CSV", str(default), "CSV (*.csv)")
        if not path:
            return
        self.service.export_table_to_csv(self.payload["title"], self.payload["tables"][0], Path(path))
        QMessageBox.information(self, "خروجی", "فایل CSV با موفقیت ذخیره شد.")

    def export_pdf(self) -> None:
        default = EXPORT_DIR / f"{self.module_key}.pdf"
        path, _ = QFileDialog.getSaveFileName(self, "ذخیره PDF", str(default), "PDF (*.pdf)")
        if not path:
            return
        html = [f"<h1>{escape(self.payload.get('title', ''))}</h1>", f"<p>{escape(self.payload.get('subtitle', ''))}</p>"]
        for card in self.payload.get("cards", []):
            html.append(f"<p><strong>{escape(card['label'])}</strong>: {escape(card['value'])}</p>")
        for table in self.payload.get("tables", []):
            html.append(f"<h2>{escape(table.get('title', ''))}</h2><table border='1' cellspacing='0' cellpadding='5' width='100%'>")
            if table.get("columns"):
                html.append("<tr>" + "".join(f"<th>{escape(str(col))}</th>" for col in table["columns"]) + "</tr>")
            for row in table.get("rows", []):
                html.append("<tr>" + "".join(f"<td>{escape(str(cell))}</td>" for cell in row) + "</tr>")
            html.append("</table>")
        if self.payload.get("insights"):
            html.append("<h2>نکات مدیریتی</h2><ul>")
            for insight in self.payload["insights"]:
                html.append(f"<li>{escape(insight)}</li>")
            html.append("</ul>")
        printer = QPrinter(QPrinter.HighResolution)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(path)
        document = QTextDocument()
        document.setHtml("".join(html))
        document.print_(printer)
        QMessageBox.information(self, "خروجی", "گزارش PDF ایجاد شد.")


class MainWindow(QMainWindow):
    def __init__(self, service: ShakarService, user: AuthenticatedUser) -> None:
        super().__init__()
        self.service = service
        self.user = user
        self.pages: dict[str, ModulePage] = {}
        self.current_module = "dashboard"
        self.setWindowTitle(f"{APP_NAME} — {user.full_name}")
        self.setMinimumSize(*WINDOW_MIN_SIZE)

        root = QWidget()
        self.setCentralWidget(root)
        layout = QHBoxLayout(root)

        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(260)
        sidebar_layout = QVBoxLayout(self.sidebar)
        app_title = QLabel(APP_NAME)
        app_title.setObjectName("Title")
        sidebar_layout.addWidget(app_title)
        sidebar_layout.addWidget(QLabel(f"{user.full_name}\n{user.role} • {user.branch_name}"))

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        for item in self.service.navigation_for(user):
            button = QPushButton(item["title"])
            button.setObjectName("SidebarButton")
            button.setCheckable(True)
            button.clicked.connect(lambda checked=False, key=item["key"]: self.show_module(key))
            self.button_group.addButton(button)
            sidebar_layout.addWidget(button)
            if item["key"] == self.current_module:
                button.setChecked(True)
        sidebar_layout.addStretch(1)
        backup_action = QPushButton("پشتیبان‌گیری فوری")
        backup_action.setProperty("variant", "ghost")
        backup_action.clicked.connect(lambda: self._handle_action("backup"))
        sidebar_layout.addWidget(backup_action)
        layout.addWidget(self.sidebar)

        self.content_host = QWidget()
        self.content_layout = QVBoxLayout(self.content_host)
        layout.addWidget(self.content_host)
        self.show_module(self.current_module)

    def show_module(self, module_key: str) -> None:
        self.current_module = module_key
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
        page = self.pages.get(module_key)
        if page is None:
            page = ModulePage(self.service, self.user, module_key, self._handle_action)
            self.pages[module_key] = page
        else:
            page.refresh()
        self.content_layout.addWidget(page)

    def _show_success(self, message: str) -> None:
        QMessageBox.information(self, "عملیات موفق", message)
        for page in self.pages.values():
            page.refresh()

    def _handle_action(self, action_code: str) -> None:
        try:
            if action_code == "new_customer":
                dialog = SimpleFormDialog("ثبت مشتری جدید", [
                    {"name": "name", "label": "نام", "type": "text"},
                    {"name": "mobile", "label": "موبایل", "type": "text"},
                    {"name": "city", "label": "شهر", "type": "text"},
                    {"name": "loyalty_tier", "label": "سطح مشتری", "type": "select", "options": [("جدید", "جدید"), ("برنزی", "برنزی"), ("نقره‌ای", "نقره‌ای"), ("طلایی", "طلایی")]},
                    {"name": "credit_limit", "label": "سقف اعتبار", "type": "float", "value": 0.0, "step": 1000000.0},
                    {"name": "notes", "label": "یادداشت", "type": "multiline"},
                ], self)
                if dialog.exec() == QDialog.Accepted:
                    self.service.create_customer(actor=self.user.username, **dialog.values())
                    self._show_success("مشتری با موفقیت ثبت شد.")
            elif action_code == "new_user":
                roles = [(role["name"], role["name"]) for role in self.service.list_roles()]
                branches = [(branch["id"], branch["name"]) for branch in self.service.list_branches()]
                dialog = SimpleFormDialog("ایجاد کاربر", [
                    {"name": "username", "label": "نام کاربری", "type": "text"},
                    {"name": "email", "label": "ایمیل", "type": "text"},
                    {"name": "full_name", "label": "نام کامل", "type": "text"},
                    {"name": "password", "label": "رمز عبور", "type": "text", "password": True},
                    {"name": "role_name", "label": "نقش", "type": "select", "options": roles},
                    {"name": "branch_id", "label": "شعبه", "type": "select", "options": branches},
                    {"name": "is_super_admin", "label": "سوپرادمین", "type": "bool"},
                ], self)
                if dialog.exec() == QDialog.Accepted:
                    self.service.create_user(actor=self.user.username, **dialog.values())
                    self._show_success("کاربر جدید با موفقیت ایجاد شد.")
            elif action_code == "new_expense":
                branches = [(branch["id"], branch["name"]) for branch in self.service.list_branches()]
                funds = [(fund["id"], f"{fund['name']} ({self.service.format_currency(fund['balance'])})") for fund in self.service.list_funds()]
                dialog = SimpleFormDialog("ثبت هزینه", [
                    {"name": "title", "label": "عنوان", "type": "text"},
                    {"name": "branch_id", "label": "شعبه", "type": "select", "options": branches, "value": self.user.branch_id},
                    {"name": "category", "label": "دسته", "type": "select", "options": [("عملیات", "عملیات"), ("بازاریابی", "بازاریابی"), ("حقوق", "حقوق"), ("اداری", "اداری")]},
                    {"name": "amount", "label": "مبلغ", "type": "float", "value": 0.0, "step": 500000.0},
                    {"name": "fund_id", "label": "صندوق/بانک", "type": "select", "options": funds},
                    {"name": "approved_by", "label": "تاییدکننده", "type": "text", "value": self.user.full_name},
                    {"name": "notes", "label": "توضیحات", "type": "multiline"},
                ], self)
                if dialog.exec() == QDialog.Accepted:
                    self.service.record_expense(actor=self.user.username, **dialog.values())
                    self._show_success("هزینه با موفقیت ثبت شد.")
            elif action_code == "new_repair":
                customers = [(None, "بدون مشتری ثبت‌شده")] + [(customer["id"], customer["name"]) for customer in self.service.list_customers()]
                dialog = SimpleFormDialog("پذیرش تعمیر", [
                    {"name": "customer_id", "label": "مشتری", "type": "select", "options": customers},
                    {"name": "device_model", "label": "مدل دستگاه", "type": "text"},
                    {"name": "imei_or_serial", "label": "IMEI / سریال", "type": "text"},
                    {"name": "issue_summary", "label": "شرح ایراد", "type": "multiline"},
                    {"name": "estimated_cost", "label": "برآورد هزینه", "type": "float", "value": 0.0, "step": 200000.0},
                    {"name": "technician", "label": "تکنسین", "type": "text"},
                    {"name": "warranty_claim", "label": "درخواست گارانتی", "type": "bool"},
                ], self)
                if dialog.exec() == QDialog.Accepted:
                    self.service.record_repair(actor=self.user.username, **dialog.values())
                    self._show_success("پذیرش تعمیر ثبت شد.")
            elif action_code == "new_sale":
                customers = [(customer["id"], customer["name"]) for customer in self.service.list_customers()]
                products = [(product["id"], f"{product['name']} | موجودی {product['stock_quantity']}") for product in self.service.list_products()]
                dialog = SimpleFormDialog("ثبت فروش سریع", [
                    {"name": "customer_id", "label": "مشتری", "type": "select", "options": customers},
                    {"name": "product_id", "label": "کالا", "type": "select", "options": products},
                    {"name": "quantity", "label": "تعداد", "type": "int", "value": 1, "min": 1, "max": 20},
                    {"name": "payment_type", "label": "نوع پرداخت", "type": "select", "options": [("cash", "نقدی"), ("installment", "اقساطی")]},
                    {"name": "down_payment", "label": "پیش‌پرداخت", "type": "float", "value": 0.0, "step": 1000000.0},
                    {"name": "installment_count", "label": "تعداد اقساط", "type": "int", "value": 3, "min": 1, "max": 12},
                    {"name": "notes", "label": "توضیحات", "type": "multiline"},
                ], self)
                if dialog.exec() == QDialog.Accepted:
                    invoice = self.service.record_sale(user=self.user, **dialog.values())
                    self._show_success(f"فروش {invoice} با موفقیت ثبت شد.")
            elif action_code == "backup":
                path = self.service.create_backup(self.user.username)
                self._show_success(f"نسخه پشتیبان در {path} ذخیره شد.")
            elif action_code == "restore":
                file_name, _ = QFileDialog.getOpenFileName(self, "انتخاب بکاپ", str(BACKUP_DIR), "Database (*.db)")
                if file_name:
                    self.service.restore_backup(Path(file_name), self.user.username)
                    self._show_success("بکاپ با موفقیت بازیابی شد.")
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "خطا", str(exc))
