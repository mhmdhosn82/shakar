from __future__ import annotations

import csv
import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from .config import DATABASE_PATH, MODULE_TITLES, ROLE_PERMISSIONS
from .database import create_backup_copy, db_connection, initialize_database, restore_backup_copy, utcnow
from .security import hash_password, verify_password


@dataclass(slots=True)
class AuthenticatedUser:
    id: int
    username: str
    full_name: str
    email: str
    role: str
    branch_id: int
    branch_name: str
    is_super_admin: bool


class ShakarService:
    def __init__(self, db_path: Path = DATABASE_PATH) -> None:
        self.db_path = Path(db_path)
        initialize_database(self.db_path)

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _fetchall(self, query: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
        with self._connect() as connection:
            return [dict(row) for row in connection.execute(query, params).fetchall()]

    def _fetchone(self, query: str, params: tuple[Any, ...] = ()) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(query, params).fetchone()
            return dict(row) if row else None

    def _execute(self, query: str, params: tuple[Any, ...] = ()) -> int:
        with self._connect() as connection:
            cursor = connection.execute(query, params)
            connection.commit()
            return int(cursor.lastrowid)

    def _executemany(self, statements: list[tuple[str, tuple[Any, ...]]]) -> None:
        with self._connect() as connection:
            for query, params in statements:
                connection.execute(query, params)
            connection.commit()

    def _audit(self, username: str, action: str, details: str) -> None:
        self._execute(
            "INSERT INTO audit_logs(username, action, details, created_at) VALUES (?, ?, ?, ?)",
            (username, action, details, utcnow()),
        )

    @staticmethod
    def format_currency(value: Any) -> str:
        try:
            return f"{float(value):,.0f} ریال"
        except (TypeError, ValueError):
            return str(value)

    @staticmethod
    def format_number(value: Any) -> str:
        try:
            return f"{float(value):,.0f}"
        except (TypeError, ValueError):
            return str(value)

    def authenticate(self, username_or_email: str, password: str) -> AuthenticatedUser | None:
        row = self._fetchone(
            """
            SELECT users.id, users.username, users.full_name, users.email, users.password_hash,
                   roles.name AS role, users.branch_id, branches.name AS branch_name, users.is_super_admin, users.is_active
            FROM users
            JOIN roles ON roles.id = users.role_id
            JOIN branches ON branches.id = users.branch_id
            WHERE users.username = ? OR users.email = ?
            """,
            (username_or_email, username_or_email),
        )
        if not row or not row["is_active"] or not verify_password(password, row["password_hash"]):
            return None
        self._audit(row["username"], "login", "ورود موفق به نرم‌افزار دسکتاپ")
        return AuthenticatedUser(
            id=row["id"],
            username=row["username"],
            full_name=row["full_name"],
            email=row["email"],
            role=row["role"],
            branch_id=row["branch_id"],
            branch_name=row["branch_name"],
            is_super_admin=bool(row["is_super_admin"]),
        )

    def has_permission(self, user: AuthenticatedUser, module_key: str) -> bool:
        allowed = ROLE_PERMISSIONS.get(user.role, set())
        return user.is_super_admin or "*" in allowed or module_key in allowed

    def navigation_for(self, user: AuthenticatedUser) -> list[dict[str, str]]:
        items = []
        for key, title in MODULE_TITLES.items():
            if self.has_permission(user, key):
                items.append({"key": key, "title": title})
        return items

    def _rows_to_table(self, title: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
        if not rows:
            return {"title": title, "columns": [], "rows": []}
        columns = list(rows[0].keys())
        table_rows = [[self._normalize_cell(row.get(column)) for column in columns] for row in rows]
        return {"title": title, "columns": columns, "rows": table_rows}

    def _normalize_cell(self, value: Any) -> str:
        if value is None:
            return "—"
        if isinstance(value, (int, float)) and abs(value) >= 1000:
            return self.format_number(value)
        if isinstance(value, (list, dict)):
            return json.dumps(value, ensure_ascii=False)
        return str(value)

    def list_customers(self) -> list[dict[str, Any]]:
        return self._fetchall("SELECT id, name, mobile FROM customers ORDER BY name")

    def list_products(self) -> list[dict[str, Any]]:
        return self._fetchall("SELECT id, sku, name, stock_quantity, sale_price, imei_required FROM products WHERE is_active = 1 ORDER BY name")

    def list_roles(self) -> list[dict[str, Any]]:
        return self._fetchall("SELECT id, name, description FROM roles ORDER BY level DESC")

    def list_branches(self) -> list[dict[str, Any]]:
        return self._fetchall("SELECT id, name, code FROM branches WHERE is_active = 1 ORDER BY name")

    def list_funds(self, branch_id: int | None = None) -> list[dict[str, Any]]:
        query = "SELECT id, name, fund_type, balance FROM funds"
        params: tuple[Any, ...] = ()
        if branch_id is not None:
            query += " WHERE branch_id = ?"
            params = (branch_id,)
        query += " ORDER BY name"
        return self._fetchall(query, params)

    def create_customer(self, *, name: str, mobile: str, city: str, loyalty_tier: str, credit_limit: float, notes: str, actor: str) -> None:
        self._execute(
            "INSERT INTO customers(name, mobile, city, loyalty_tier, credit_limit, balance, notes) VALUES (?, ?, ?, ?, ?, 0, ?)",
            (name.strip(), mobile.strip(), city.strip(), loyalty_tier.strip() or "جدید", credit_limit, notes.strip()),
        )
        self._audit(actor, "create_customer", f"ثبت مشتری {name}")

    def create_user(self, *, username: str, email: str, full_name: str, password: str, role_name: str, branch_id: int, is_super_admin: bool, actor: str) -> None:
        role = self._fetchone("SELECT id FROM roles WHERE name = ?", (role_name,))
        if role is None:
            raise ValueError("نقش انتخاب‌شده معتبر نیست")
        self._execute(
            "INSERT INTO users(username, email, full_name, password_hash, role_id, branch_id, is_active, is_super_admin, created_at) VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?)",
            (username.strip(), email.strip(), full_name.strip(), hash_password(password), role["id"], branch_id, int(is_super_admin), utcnow()),
        )
        self._audit(actor, "create_user", f"ایجاد کاربر {username}")

    def _next_document_no(self, prefix: str, table: str, field: str) -> str:
        row = self._fetchone(f"SELECT {field} AS value FROM {table} WHERE {field} LIKE ? ORDER BY id DESC LIMIT 1", (f"{prefix}%",))
        if not row:
            return f"{prefix}-0001"
        last = str(row["value"]).split("-")[-1]
        return f"{prefix}-{int(last) + 1:04d}"

    def record_repair(self, *, customer_id: int | None, device_model: str, imei_or_serial: str, issue_summary: str, estimated_cost: float, technician: str, warranty_claim: bool, actor: str) -> None:
        ticket_no = self._next_document_no("REP", "repairs", "ticket_no")
        self._execute(
            "INSERT INTO repairs(ticket_no, customer_id, device_model, imei_or_serial, issue_summary, estimated_cost, status, received_at, technician, warranty_claim) VALUES (?, ?, ?, ?, ?, ?, 'received', ?, ?, ?)",
            (ticket_no, customer_id, device_model.strip(), imei_or_serial.strip(), issue_summary.strip(), estimated_cost, utcnow(), technician.strip(), int(warranty_claim)),
        )
        self._audit(actor, "register_repair", f"ثبت پذیرش تعمیر {ticket_no}")

    def record_expense(self, *, title: str, branch_id: int, category: str, amount: float, fund_id: int, approved_by: str, notes: str, actor: str) -> None:
        fund = self._fetchone("SELECT * FROM funds WHERE id = ?", (fund_id,))
        if fund is None:
            raise ValueError("صندوق انتخاب‌شده وجود ندارد")
        if float(fund["balance"]) < amount:
            raise ValueError("موجودی صندوق برای این هزینه کافی نیست")
        with self._connect() as connection:
            expense_id = connection.execute(
                "INSERT INTO expenses(title, branch_id, category, amount, expense_date, paid_from_fund_id, approved_by, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (title.strip(), branch_id, category.strip(), amount, utcnow(), fund_id, approved_by.strip(), notes.strip()),
            ).lastrowid
            connection.execute("UPDATE funds SET balance = balance - ? WHERE id = ?", (amount, fund_id))
            connection.execute(
                "INSERT INTO payments(source_type, source_id, direction, fund_id, amount, method, paid_at, note) VALUES ('expense', ?, 'out', ?, ?, 'cash', ?, ?)",
                (expense_id, fund_id, amount, utcnow(), title.strip()),
            )
            entry_no = self._next_document_no("JE-EXP", "journal_entries", "entry_no")
            expense_account = connection.execute("SELECT id FROM accounts WHERE code = '6100'").fetchone()[0]
            fund_account_code = "1000" if fund["fund_type"] == "cash" else "1100"
            fund_account = connection.execute("SELECT id FROM accounts WHERE code = ?", (fund_account_code,)).fetchone()[0]
            entry_id = connection.execute(
                "INSERT INTO journal_entries(entry_no, branch_id, entry_date, description, total_debit, total_credit, status) VALUES (?, ?, ?, ?, ?, ?, 'posted')",
                (entry_no, branch_id, utcnow(), title.strip(), amount, amount),
            ).lastrowid
            connection.executemany(
                "INSERT INTO journal_lines(entry_id, account_id, debit, credit, description) VALUES (?, ?, ?, ?, ?)",
                [(entry_id, expense_account, amount, 0, title.strip()), (entry_id, fund_account, 0, amount, title.strip())],
            )
            connection.execute("UPDATE accounts SET balance = balance + ? WHERE code = '6100'", (amount,))
            connection.execute("UPDATE accounts SET balance = balance - ? WHERE code = ?", (amount, fund_account_code))
            connection.commit()
        self._audit(actor, "record_expense", f"ثبت هزینه {title}")

    def record_sale(
        self,
        *,
        customer_id: int,
        product_id: int,
        quantity: int,
        payment_type: str,
        user: AuthenticatedUser,
        down_payment: float,
        installment_count: int,
        notes: str,
    ) -> str:
        if quantity <= 0:
            raise ValueError("تعداد باید بیشتر از صفر باشد")
        with self._connect() as connection:
            product = connection.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
            if product is None:
                raise ValueError("کالا یافت نشد")
            if product["stock_quantity"] < quantity:
                raise ValueError("موجودی کافی نیست")
            invoice_no = self._next_document_no("SAL", "sales", "invoice_no")
            total = float(product["sale_price"]) * quantity
            cost_total = float(product["cost_price"]) * quantity
            profit = total - cost_total
            paid = total if payment_type == "cash" else min(down_payment, total)
            sale_id = connection.execute(
                "INSERT INTO sales(invoice_no, customer_id, branch_id, salesperson_id, sold_at, total, paid, profit, payment_type, status, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'confirmed', ?)",
                (invoice_no, customer_id, user.branch_id, user.id, utcnow(), total, paid, profit, payment_type, notes.strip()),
            ).lastrowid
            imei_id = None
            if product["imei_required"]:
                imei_row = connection.execute(
                    "SELECT id FROM imei_items WHERE product_id = ? AND status = 'in_stock' ORDER BY id LIMIT 1",
                    (product_id,),
                ).fetchone()
                if imei_row is None:
                    raise ValueError("IMEI آزاد برای این گوشی موجود نیست")
                imei_id = int(imei_row[0])
                connection.execute("UPDATE imei_items SET status = 'sold' WHERE id = ?", (imei_id,))
            connection.execute(
                "INSERT INTO sale_items(sale_id, product_id, qty, unit_price, line_total, imei_id) VALUES (?, ?, ?, ?, ?, ?)",
                (sale_id, product_id, quantity, float(product["sale_price"]), total, imei_id),
            )
            connection.execute("UPDATE products SET stock_quantity = stock_quantity - ?, last_sold_at = ? WHERE id = ?", (quantity, utcnow(), product_id))
            fund = connection.execute("SELECT id, fund_type FROM funds WHERE branch_id = ? ORDER BY id LIMIT 1", (user.branch_id,)).fetchone()
            if paid > 0 and fund:
                connection.execute("UPDATE funds SET balance = balance + ? WHERE id = ?", (paid, int(fund[0])))
                connection.execute(
                    "INSERT INTO payments(source_type, source_id, direction, fund_id, amount, method, paid_at, note) VALUES ('sale', ?, 'in', ?, ?, ?, ?, ?)",
                    (sale_id, int(fund[0]), paid, 'cash' if payment_type == 'cash' else 'installment', utcnow(), invoice_no),
                )
            due = total - paid
            if due > 0:
                connection.execute("UPDATE customers SET balance = balance + ? WHERE id = ?", (due, customer_id))
                installment_amount = round(due / max(installment_count, 1), 2)
                plan_id = connection.execute(
                    "INSERT INTO installment_plans(sale_id, down_payment, installment_amount, installment_count, interest_rate, remaining_amount, status) VALUES (?, ?, ?, ?, ?, ?, 'active')",
                    (sale_id, paid, installment_amount, installment_count, 0, due),
                ).lastrowid
                for index in range(max(installment_count, 1)):
                    due_date = (datetime.utcnow() + timedelta(days=30 * (index + 1))).replace(microsecond=0).isoformat(sep=' ')
                    connection.execute(
                        "INSERT INTO installment_schedules(plan_id, due_date, amount, paid_amount, status) VALUES (?, ?, ?, 0, 'pending')",
                        (plan_id, due_date, installment_amount),
                    )
            entry_no = self._next_document_no("JE-SAL", "journal_entries", "entry_no")
            entry_id = connection.execute(
                "INSERT INTO journal_entries(entry_no, branch_id, entry_date, description, total_debit, total_credit, status) VALUES (?, ?, ?, ?, ?, ?, 'posted')",
                (entry_no, user.branch_id, utcnow(), f"فروش {invoice_no}", total + cost_total, total + cost_total),
            ).lastrowid
            account_codes = {row['code']: row['id'] for row in connection.execute("SELECT id, code FROM accounts")}
            lines = []
            if paid > 0:
                lines.append((entry_id, account_codes['1000'], paid, 0, f"وصول {invoice_no}"))
                connection.execute("UPDATE accounts SET balance = balance + ? WHERE code = '1000'", (paid,))
            if due > 0:
                lines.append((entry_id, account_codes['1200'], due, 0, f"مطالبات {invoice_no}"))
                connection.execute("UPDATE accounts SET balance = balance + ? WHERE code = '1200'", (due,))
            lines.extend([
                (entry_id, account_codes['4000'], 0, total, f"درآمد {invoice_no}"),
                (entry_id, account_codes['5000'], cost_total, 0, f"بهای تمام‌شده {invoice_no}"),
                (entry_id, account_codes['1300'], 0, cost_total, f"کاهش موجودی {invoice_no}"),
            ])
            connection.executemany("INSERT INTO journal_lines(entry_id, account_id, debit, credit, description) VALUES (?, ?, ?, ?, ?)", lines)
            connection.execute("UPDATE accounts SET balance = balance - ? WHERE code = '4000'", (total,))
            connection.execute("UPDATE accounts SET balance = balance + ? WHERE code = '5000'", (cost_total,))
            connection.execute("UPDATE accounts SET balance = balance - ? WHERE code = '1300'", (cost_total,))
            connection.commit()
        self._audit(user.username, "record_sale", f"ثبت فروش {invoice_no}")
        return invoice_no

    def create_backup(self, actor: str) -> Path:
        path = create_backup_copy(self.db_path, actor=actor)
        self._audit(actor, "backup", f"پشتیبان‌گیری در {path.name}")
        return path

    def restore_backup(self, source: Path, actor: str) -> None:
        restore_backup_copy(source, self.db_path)
        self._audit(actor, "restore", f"بازیابی نسخه پشتیبان {source.name}")

    def export_table_to_csv(self, title: str, table: dict[str, Any], path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.writer(handle)
            if title:
                writer.writerow([title])
            if table["columns"]:
                writer.writerow(table["columns"])
            writer.writerows(table["rows"])

    def get_payload(self, module_key: str, user: AuthenticatedUser) -> dict[str, Any]:
        if not self.has_permission(user, module_key):
            return {"title": MODULE_TITLES[module_key], "subtitle": "شما به این بخش دسترسی ندارید.", "cards": [], "tables": [], "insights": ["برای این ماژول باید نقش بالاتری داشته باشید."], "actions": []}
        builder = getattr(self, f"_payload_{module_key}", None)
        if builder is None:
            return {"title": MODULE_TITLES[module_key], "subtitle": "این بخش در حال آماده‌سازی است.", "cards": [], "tables": [], "insights": [], "actions": []}
        return builder(user)

    def _summary_cards(self) -> list[dict[str, str]]:
        totals = self._fetchone(
            """
            SELECT
                COALESCE((SELECT SUM(total) FROM sales), 0) AS total_sales,
                COALESCE((SELECT SUM(profit) FROM sales), 0) AS gross_profit,
                COALESCE((SELECT COUNT(*) FROM products WHERE stock_quantity <= reorder_point), 0) AS low_stock,
                COALESCE((SELECT COUNT(*) FROM installment_schedules WHERE status != 'paid' AND due_date < datetime('now')), 0) AS overdue_installments,
                COALESCE((SELECT COUNT(*) FROM repairs WHERE status NOT IN ('delivered', 'closed')), 0) AS open_repairs,
                COALESCE((SELECT SUM(balance) FROM funds), 0) AS fund_balance
            """
        ) or {}
        return [
            {"label": "فروش کل", "value": self.format_currency(totals.get("total_sales", 0)), "tone": "primary"},
            {"label": "سود ناخالص", "value": self.format_currency(totals.get("gross_profit", 0)), "tone": "success"},
            {"label": "کمبود موجودی", "value": str(totals.get("low_stock", 0)), "tone": "warning"},
            {"label": "اقساط سررسید گذشته", "value": str(totals.get("overdue_installments", 0)), "tone": "danger"},
            {"label": "تعمیرات باز", "value": str(totals.get("open_repairs", 0)), "tone": "neutral"},
            {"label": "مانده وجوه", "value": self.format_currency(totals.get("fund_balance", 0)), "tone": "info"},
        ]

    def _low_stock_rows(self) -> list[dict[str, Any]]:
        return self._fetchall(
            "SELECT sku AS کد, name AS کالا, stock_quantity AS موجودی, reorder_point AS نقطه_سفارش, sale_price AS قیمت_فروش FROM products WHERE stock_quantity <= reorder_point ORDER BY stock_quantity ASC"
        )

    def _purchase_recommendations(self) -> list[dict[str, Any]]:
        rows = self._fetchall(
            """
            SELECT p.sku, p.name, p.stock_quantity, p.reorder_point,
                   COALESCE(SUM(si.qty), 0) AS sold_qty_30d,
                   ROUND(COALESCE(SUM(si.qty), 0) / 30.0, 2) AS daily_velocity
            FROM products p
            LEFT JOIN sale_items si ON si.product_id = p.id
            LEFT JOIN sales s ON s.id = si.sale_id AND s.sold_at >= datetime('now', '-30 day')
            GROUP BY p.id
            HAVING p.stock_quantity <= p.reorder_point OR daily_velocity > 0.2
            ORDER BY daily_velocity DESC, p.stock_quantity ASC
            """
        )
        recommendations = []
        for row in rows:
            target = max(int(row["reorder_point"] or 0) * 2, int((row["daily_velocity"] or 0) * 14))
            suggested = max(target - int(row["stock_quantity"] or 0), 0)
            if suggested > 0:
                recommendations.append({"SKU": row["sku"], "کالا": row["name"], "موجودی": row["stock_quantity"], "فروش_30_روز": row["sold_qty_30d"], "پیشنهاد_خرید": suggested})
        return recommendations[:8]

    def _stagnant_rows(self) -> list[dict[str, Any]]:
        return self._fetchall(
            "SELECT sku AS SKU, name AS کالا, stock_quantity AS موجودی, COALESCE(last_sold_at, 'بدون فروش') AS آخرین_فروش FROM products WHERE stock_quantity > 0 AND (last_sold_at IS NULL OR last_sold_at < datetime('now', '-30 day')) ORDER BY stock_quantity DESC"
        )

    def _payload_dashboard(self, user: AuthenticatedUser) -> dict[str, Any]:
        top_products = self._fetchall(
            """
            SELECT p.name AS کالا, SUM(si.qty) AS تعداد_فروش, SUM(si.line_total) AS مبلغ
            FROM sale_items si
            JOIN products p ON p.id = si.product_id
            JOIN sales s ON s.id = si.sale_id
            WHERE s.sold_at >= datetime('now', '-30 day')
            GROUP BY p.id
            ORDER BY SUM(si.line_total) DESC
            LIMIT 6
            """
        )
        branch_performance = self._fetchall(
            """
            SELECT b.name AS شعبه, COALESCE(SUM(s.total), 0) AS فروش, COALESCE(SUM(s.profit), 0) AS سود
            FROM branches b
            LEFT JOIN sales s ON s.branch_id = b.id
            GROUP BY b.id
            ORDER BY فروش DESC
            """
        )
        insights = [
            "موتور هوشمند خرید بر اساس سرعت فروش ۳۰ روزه و نقطه سفارش مجدد پیشنهاد می‌دهد.",
            "اقساط سررسید گذشته مستقیماً در تحلیل نقدینگی و پیگیری مطالبات لحاظ شده‌اند.",
            "سازگاری اکسسوری با مدل‌های موبایل در کاتالوگ ذخیره شده و برای فروش مکمل استفاده می‌شود.",
        ]
        recommendations = self._purchase_recommendations()
        if recommendations:
            insights.append(f"پیشنهاد فوری: {recommendations[0]['کالا']} با پیشنهاد خرید {recommendations[0]['پیشنهاد_خرید']} عدد در اولویت تامین است.")
        return {
            "title": MODULE_TITLES["dashboard"],
            "subtitle": f"خوش آمدید {user.full_name} — نمای زنده مدیریت فروشگاه {user.branch_name}",
            "cards": self._summary_cards(),
            "tables": [self._rows_to_table("محصولات پرفروش ۳۰ روز اخیر", top_products), self._rows_to_table("عملکرد شعب", branch_performance), self._rows_to_table("پیشنهاد خرید هوشمند", recommendations)],
            "insights": insights,
            "actions": ["new_sale", "new_customer", "backup"],
        }

    def _payload_users(self, user: AuthenticatedUser) -> dict[str, Any]:
        users = self._fetchall(
            "SELECT u.username AS کاربری, u.full_name AS نام, u.email AS ایمیل, r.name AS نقش, b.name AS شعبه, CASE WHEN u.is_super_admin = 1 THEN 'بله' ELSE 'خیر' END AS سوپرادمین FROM users u JOIN roles r ON r.id = u.role_id JOIN branches b ON b.id = u.branch_id ORDER BY u.is_super_admin DESC, r.level DESC"
        )
        recent_audit = self._fetchall("SELECT username AS کاربر, action AS اقدام, details AS جزئیات, created_at AS زمان FROM audit_logs ORDER BY id DESC LIMIT 10")
        return {
            "title": MODULE_TITLES["users"],
            "subtitle": "احراز هویت، کاربران و کنترل سطح دسترسی مدیران و شعب",
            "cards": [{"label": "کل کاربران فعال", "value": str(len(users)), "tone": "primary"}, {"label": "ورود پیش‌فرض", "value": "admin / Admin@123456", "tone": "info"}],
            "tables": [self._rows_to_table("کاربران سیستم", users), self._rows_to_table("ثبت رویدادهای اخیر", recent_audit)],
            "insights": ["سوپرادمین می‌تواند همه ماژول‌ها را مشاهده و کاربر جدید ایجاد کند.", "رویدادهای مهم ورود، پشتیبان‌گیری و عملیات کلیدی ثبت می‌شوند."],
            "actions": ["new_user"],
        }

    def _payload_roles(self, user: AuthenticatedUser) -> dict[str, Any]:
        rows = self._fetchall(
            "SELECT r.name AS نقش, r.description AS توضیح, GROUP_CONCAT(p.title, '، ') AS دسترسی‌ها FROM roles r LEFT JOIN role_permissions rp ON rp.role_id = r.id LEFT JOIN permissions p ON p.id = rp.permission_id GROUP BY r.id ORDER BY r.level DESC"
        )
        return {
            "title": MODULE_TITLES["roles"],
            "subtitle": "مدل دسترسی مبتنی بر نقش برای مدیریت کامل فروشگاه",
            "cards": [{"label": "تعداد نقش‌ها", "value": str(len(rows)), "tone": "primary"}],
            "tables": [self._rows_to_table("نقش‌ها و مجوزها", rows)],
            "insights": ["نقش manager برای کنترل عملیات روزانه و گزارش‌ها تعریف شده است.", "نقش accountant روی گردش‌های مالی، حسابداری و گزارش‌های مالی تمرکز دارد."],
            "actions": [],
        }

    def _payload_branches(self, user: AuthenticatedUser) -> dict[str, Any]:
        branches = self._fetchall("SELECT name AS شعبه, code AS کد, manager_name AS مدیر, city AS شهر, phone AS تماس FROM branches ORDER BY id")
        warehouses = self._fetchall("SELECT w.name AS انبار, w.code AS کد, b.name AS شعبه, w.capacity AS ظرفیت, w.notes AS توضیح FROM warehouses w JOIN branches b ON b.id = w.branch_id ORDER BY b.id")
        return {
            "title": MODULE_TITLES["branches"],
            "subtitle": "کنترل چند شعبه‌ای، مدیر هر شعبه و ظرفیت انبارها",
            "cards": [{"label": "شعب فعال", "value": str(len(branches)), "tone": "primary"}, {"label": "انبارها", "value": str(len(warehouses)), "tone": "info"}],
            "tables": [self._rows_to_table("شعب فروشگاه", branches), self._rows_to_table("انبارها", warehouses)],
            "insights": ["شعبه مرکزی روی گوشی‌های رجیسترشده متمرکز است و کرج روی اکسسوری و فروش سریع.", "برای هر شعبه صندوق و جریان نقدی مستقل نگهداری می‌شود."],
            "actions": [],
        }

    def _payload_inventory(self, user: AuthenticatedUser) -> dict[str, Any]:
        inventory = self._fetchall(
            "SELECT sku AS SKU, name AS کالا, stock_quantity AS موجودی, reorder_point AS نقطه_سفارش, CASE WHEN imei_required = 1 THEN 'IMEI' ELSE 'عادی' END AS نوع FROM products ORDER BY stock_quantity ASC"
        )
        imeis = self._fetchall("SELECT p.name AS کالا, i.imei AS IMEI, i.status AS وضعیت, i.warranty_until AS پایان_گارانتی FROM imei_items i JOIN products p ON p.id = i.product_id ORDER BY i.id DESC")
        return {
            "title": MODULE_TITLES["inventory"],
            "subtitle": "کنترل موجودی، انبار، هشدار کمبود و ردیابی IMEI/سریال",
            "cards": [{"label": "اقلام کم‌موجود", "value": str(len(self._low_stock_rows())), "tone": "warning"}, {"label": "IMEI ثبت‌شده", "value": str(len(imeis)), "tone": "primary"}],
            "tables": [self._rows_to_table("موجودی کالا", inventory), self._rows_to_table("ردیابی IMEI / سریال", imeis), self._rows_to_table("هشدار کمبود موجودی", self._low_stock_rows())],
            "insights": ["برای گوشی‌ها ردیابی تک‌به‌تک IMEI انجام می‌شود.", "کالاهای راکد برای تصمیم‌گیری تخفیف یا باندل در گزارش هوشمند نمایش داده می‌شوند."],
            "actions": ["new_sale"],
        }

    def _payload_catalog(self, user: AuthenticatedUser) -> dict[str, Any]:
        products = self._fetchall(
            "SELECT p.sku AS SKU, p.name AS کالا, b.name AS برند, p.product_type AS نوع, p.sale_price AS قیمت_فروش, p.bundle_offer AS باندل FROM products p LEFT JOIN brands b ON b.id = p.brand_id ORDER BY p.product_type, p.name"
        )
        compatibility = []
        for row in self._fetchall("SELECT sku, name, compatible_devices, cross_sell_skus FROM products WHERE product_type = 'accessory' ORDER BY trend_score DESC"):
            compatibility.append({
                "SKU": row["sku"],
                "اکسسوری": row["name"],
                "سازگار_با": "، ".join(json.loads(row["compatible_devices"])),
                "پیشنهاد_فروش_مکمل": "، ".join(json.loads(row["cross_sell_skus"])),
            })
        return {
            "title": MODULE_TITLES["catalog"],
            "subtitle": "کاتالوگ موبایل و اکسسوری با سازگاری، باندل و فروش مکمل",
            "cards": [{"label": "کل SKU", "value": str(len(products)), "tone": "primary"}, {"label": "اکسسوری‌های سازگار", "value": str(len(compatibility)), "tone": "success"}],
            "tables": [self._rows_to_table("کاتالوگ کالا", products), self._rows_to_table("سازگاری و کراس‌سل اکسسوری", compatibility)],
            "insights": ["برای هر اکسسوری مدل‌های سازگار ذخیره شده‌اند تا فروشنده فروش مکمل دقیق‌تری داشته باشد.", "باندل‌های آماده برای اپل، سامسونگ و شیائومی در سیستم ثبت شده‌اند."],
            "actions": [],
        }

    def _payload_purchases(self, user: AuthenticatedUser) -> dict[str, Any]:
        purchases = self._fetchall("SELECT invoice_no AS فاکتور, s.name AS تامین‌کننده, total AS مبلغ, paid AS پرداختی, status AS وضعیت, purchased_at AS تاریخ FROM purchases p JOIN suppliers s ON s.id = p.supplier_id ORDER BY p.purchased_at DESC")
        suppliers = self._fetchall("SELECT name AS تامین‌کننده, contact_name AS رابط, mobile AS تماس, payables_balance AS بدهی, rating AS امتیاز FROM suppliers ORDER BY rating DESC")
        return {
            "title": MODULE_TITLES["purchases"],
            "subtitle": "تامین کالا، بدهی تامین‌کنندگان و پیشنهاد خرید مجدد",
            "cards": [{"label": "تامین‌کنندگان فعال", "value": str(len(suppliers)), "tone": "primary"}, {"label": "پیشنهادهای خرید", "value": str(len(self._purchase_recommendations())), "tone": "warning"}],
            "tables": [self._rows_to_table("سفارش‌های خرید", purchases), self._rows_to_table("تامین‌کنندگان", suppliers), self._rows_to_table("پیشنهاد خرید هوشمند", self._purchase_recommendations())],
            "insights": ["پیشنهاد خرید بر مبنای فروش ۳۰ روز اخیر و حداقل پوشش ۱۴ روزه محاسبه می‌شود.", "امتیاز تامین‌کنندگان برای اولویت‌بندی خریدهای بعدی ثبت شده است."],
            "actions": ["backup"],
        }

    def _payload_sales(self, user: AuthenticatedUser) -> dict[str, Any]:
        sales = self._fetchall("SELECT invoice_no AS فاکتور, c.name AS مشتری, total AS مبلغ, paid AS دریافتی, payment_type AS نوع_پرداخت, sold_at AS تاریخ FROM sales s LEFT JOIN customers c ON c.id = s.customer_id ORDER BY s.sold_at DESC")
        top = self._fetchall("SELECT p.name AS کالا, SUM(si.qty) AS تعداد, SUM(si.line_total) AS مبلغ FROM sale_items si JOIN products p ON p.id = si.product_id GROUP BY p.id ORDER BY SUM(si.line_total) DESC LIMIT 8")
        return {
            "title": MODULE_TITLES["sales"],
            "subtitle": "فروش نقدی و اقساطی، فروش مکمل و تحلیل مشتریان",
            "cards": [{"label": "فاکتورهای فروش", "value": str(len(sales)), "tone": "primary"}, {"label": "میانگین فاکتور", "value": self.format_currency(sum(float(row['مبلغ']) for row in sales) / max(len(sales), 1)), "tone": "info"}],
            "tables": [self._rows_to_table("فروش‌های ثبت‌شده", sales), self._rows_to_table("پرفروش‌ها", top)],
            "insights": ["ثبت فروش سریع از همین صفحه موجود است و موجودی را به‌صورت خودکار کاهش می‌دهد.", "برای گوشی‌ها در زمان فروش، IMEI آزاد به فروش اختصاص پیدا می‌کند."],
            "actions": ["new_sale", "new_customer"],
        }

    def _payload_installments(self, user: AuthenticatedUser) -> dict[str, Any]:
        plans = self._fetchall("SELECT s.invoice_no AS فاکتور, c.name AS مشتری, ip.remaining_amount AS مانده, ip.installment_amount AS مبلغ_قسط, ip.installment_count AS تعداد, ip.status AS وضعیت FROM installment_plans ip JOIN sales s ON s.id = ip.sale_id LEFT JOIN customers c ON c.id = s.customer_id ORDER BY ip.id DESC")
        schedules = self._fetchall("SELECT c.name AS مشتری, s.invoice_no AS فاکتور, due_date AS سررسید, amount AS مبلغ, paid_amount AS پرداختی, status AS وضعیت FROM installment_schedules sch JOIN installment_plans ip ON ip.id = sch.plan_id JOIN sales s ON s.id = ip.sale_id LEFT JOIN customers c ON c.id = s.customer_id ORDER BY due_date")
        overdue = sum(1 for row in schedules if row["وضعیت"] == "overdue")
        return {
            "title": MODULE_TITLES["installments"],
            "subtitle": "کنترل فروش اقساطی، مانده مطالبات و پیگیری سررسیدها",
            "cards": [{"label": "طرح‌های اقساطی", "value": str(len(plans)), "tone": "primary"}, {"label": "اقساط معوق", "value": str(overdue), "tone": "danger"}],
            "tables": [self._rows_to_table("طرح‌های اقساط", plans), self._rows_to_table("زمان‌بندی اقساط", schedules)],
            "insights": ["اقساط معوق باید فوراً پیگیری شوند تا فشار نقدینگی کاهش یابد.", "مانده اقساط به‌صورت خودکار به حساب‌های دریافتنی و پرونده مشتری منتقل می‌شود."],
            "actions": ["new_sale"],
        }

    def _payload_customers(self, user: AuthenticatedUser) -> dict[str, Any]:
        rows = self._fetchall("SELECT name AS مشتری, mobile AS موبایل, city AS شهر, loyalty_tier AS سطح, credit_limit AS سقف_اعتبار, balance AS مانده FROM customers ORDER BY balance DESC, name")
        return {
            "title": MODULE_TITLES["customers"],
            "subtitle": "پرونده مشتری، اعتبار، خریدهای اقساطی و وفادارسازی",
            "cards": [{"label": "کل مشتریان", "value": str(len(rows)), "tone": "primary"}, {"label": "مانده مطالبات", "value": self.format_currency(sum(float(row['مانده']) for row in rows)), "tone": "warning"}],
            "tables": [self._rows_to_table("مشتریان", rows)],
            "insights": ["مشتریان شرکتی و اقساطی در اولویت تحلیل اعتبار و پیگیری قرار دارند."],
            "actions": ["new_customer"],
        }

    def _payload_suppliers(self, user: AuthenticatedUser) -> dict[str, Any]:
        rows = self._fetchall("SELECT name AS تامین‌کننده, contact_name AS رابط, mobile AS تماس, city AS شهر, payables_balance AS مانده_بدهی, rating AS امتیاز FROM suppliers ORDER BY payables_balance DESC")
        return {
            "title": MODULE_TITLES["suppliers"],
            "subtitle": "تامین‌کنندگان اصلی موبایل و اکسسوری، امتیازدهی و بدهی باز",
            "cards": [{"label": "کل تامین‌کنندگان", "value": str(len(rows)), "tone": "primary"}],
            "tables": [self._rows_to_table("تامین‌کنندگان", rows)],
            "insights": ["مانده بدهی تامین‌کنندگان باید با برنامه پرداخت ماهانه کنترل شود."],
            "actions": [],
        }

    def _payload_payments(self, user: AuthenticatedUser) -> dict[str, Any]:
        funds = self._fetchall("SELECT f.name AS صندوق, f.fund_type AS نوع, b.name AS شعبه, f.balance AS مانده FROM funds f JOIN branches b ON b.id = f.branch_id ORDER BY b.id")
        payments = self._fetchall("SELECT source_type AS مبدا, direction AS جهت, amount AS مبلغ, method AS روش, paid_at AS تاریخ, note AS توضیح FROM payments ORDER BY paid_at DESC LIMIT 20")
        return {
            "title": MODULE_TITLES["payments"],
            "subtitle": "وجوه نقد، بانک‌ها و گردش دریافت و پرداخت",
            "cards": [{"label": "مانده کل وجوه", "value": self.format_currency(sum(float(row['مانده']) for row in funds)), "tone": "success"}],
            "tables": [self._rows_to_table("صندوق‌ها و حساب‌ها", funds), self._rows_to_table("گردش‌های اخیر", payments)],
            "insights": ["گردش صندوق و بانک به صورت لحظه‌ای برای مدیریت نقدینگی دیده می‌شود."],
            "actions": ["new_expense"],
        }

    def _payload_accounting(self, user: AuthenticatedUser) -> dict[str, Any]:
        accounts = self._fetchall("SELECT code AS کد, name AS حساب, account_type AS نوع, balance AS مانده FROM accounts ORDER BY code")
        entries = self._fetchall("SELECT entry_no AS سند, entry_date AS تاریخ, description AS شرح, total_debit AS بدهکار, total_credit AS بستانکار FROM journal_entries ORDER BY entry_date DESC")
        return {
            "title": MODULE_TITLES["accounting"],
            "subtitle": "حسابداری دوبل، اسناد مالی و مانده حساب‌ها",
            "cards": [{"label": "تعداد اسناد", "value": str(len(entries)), "tone": "primary"}, {"label": "جمع حساب‌ها", "value": self.format_currency(sum(abs(float(row['مانده'])) for row in accounts)), "tone": "info"}],
            "tables": [self._rows_to_table("حساب‌ها", accounts), self._rows_to_table("اسناد حسابداری", entries)],
            "insights": ["فروش و هزینه‌ها به‌طور خودکار سند حسابداری تولید می‌کنند.", "حساب‌های دریافتنی و موجودی کالا جزو ارکان کنترل مدیریت هستند."],
            "actions": ["new_expense"],
        }

    def _payload_expenses(self, user: AuthenticatedUser) -> dict[str, Any]:
        rows = self._fetchall("SELECT title AS هزینه, category AS دسته, amount AS مبلغ, expense_date AS تاریخ, approved_by AS تاییدکننده FROM expenses ORDER BY expense_date DESC")
        return {
            "title": MODULE_TITLES["expenses"],
            "subtitle": "ثبت هزینه‌های فروشگاه و تاثیر مستقیم بر نقدینگی و سود",
            "cards": [{"label": "هزینه کل ثبت‌شده", "value": self.format_currency(sum(float(row['مبلغ']) for row in rows)), "tone": "warning"}],
            "tables": [self._rows_to_table("هزینه‌ها", rows)],
            "insights": ["ثبت هزینه از همین صفحه امکان‌پذیر است و هم‌زمان صندوق و سند حسابداری را به‌روزرسانی می‌کند."],
            "actions": ["new_expense"],
        }

    def _payload_service(self, user: AuthenticatedUser) -> dict[str, Any]:
        returns = self._fetchall("SELECT return_no AS مرجوعی, reason AS علت, amount AS مبلغ, status AS وضعیت, opened_at AS تاریخ FROM returns ORDER BY opened_at DESC")
        repairs = self._fetchall("SELECT ticket_no AS پذیرش, device_model AS دستگاه, issue_summary AS ایراد, estimated_cost AS برآورد, status AS وضعیت, technician AS تکنسین FROM repairs ORDER BY received_at DESC")
        return {
            "title": MODULE_TITLES["service"],
            "subtitle": "مرجوعی، گارانتی و پذیرش تعمیرات فروشگاه موبایل",
            "cards": [{"label": "مرجوعی‌ها", "value": str(len(returns)), "tone": "warning"}, {"label": "تعمیرات فعال", "value": str(len([r for r in repairs if r['وضعیت'] not in ('closed', 'delivered')])), "tone": "primary"}],
            "tables": [self._rows_to_table("مرجوعی و گارانتی", returns), self._rows_to_table("تعمیرات", repairs)],
            "insights": ["پذیرش تعمیر جدید از همین بخش ثبت می‌شود.", "برای درخواست‌های گارانتی، وضعیت قطعات و تکنسین قابل پیگیری است."],
            "actions": ["new_repair"],
        }

    def _payload_reports(self, user: AuthenticatedUser) -> dict[str, Any]:
        accessory = self._fetchall(
            "SELECT p.name AS اکسسوری, SUM(si.qty) AS فروش_تعداد, SUM(si.line_total) AS فروش_مبلغ, GROUP_CONCAT(DISTINCT json_extract(p.compatible_devices, '$[0]')) AS مدل_شاخص FROM sale_items si JOIN products p ON p.id = si.product_id WHERE p.product_type = 'accessory' GROUP BY p.id ORDER BY فروش_مبلغ DESC"
        )
        insights = [
            f"{row['اکسسوری']} در اکسسوری‌ها جزو پرفروش‌ترین‌هاست." for row in accessory[:3]
        ]
        insights += [
            f"{row['کالا']} مدت‌ها فروش نداشته و برای تخفیف یا باندل مناسب است." for row in self._stagnant_rows()[:3]
        ]
        return {
            "title": MODULE_TITLES["reports"],
            "subtitle": "گزارش‌های مدیریتی، تحلیل روند اکسسوری و پیشنهادهای هوشمند خرید",
            "cards": [{"label": "گزارش‌های راکد", "value": str(len(self._stagnant_rows())), "tone": "warning"}, {"label": "پیشنهادهای خرید", "value": str(len(self._purchase_recommendations())), "tone": "primary"}],
            "tables": [self._rows_to_table("روند اکسسوری‌ها", accessory), self._rows_to_table("کالاهای راکد", self._stagnant_rows()), self._rows_to_table("پیشنهاد خرید", self._purchase_recommendations())],
            "insights": insights,
            "actions": ["backup"],
        }

    def _payload_settings(self, user: AuthenticatedUser) -> dict[str, Any]:
        settings = self._fetchall("SELECT key AS کلید, value AS مقدار, updated_at AS آخرین_به‌روزرسانی FROM settings ORDER BY key")
        backups = self._fetchall("SELECT backup_path AS فایل, created_at AS زمان, created_by AS ایجادکننده FROM backup_history ORDER BY id DESC LIMIT 10")
        return {
            "title": MODULE_TITLES["settings"],
            "subtitle": "تنظیمات اپ، دیتابیس محلی، پشتیبان‌گیری و بازیابی",
            "cards": [{"label": "مسیر دیتابیس", "value": str(self.db_path), "tone": "neutral"}, {"label": "تعداد بکاپ‌ها", "value": str(len(backups)), "tone": "primary"}],
            "tables": [self._rows_to_table("تنظیمات", settings), self._rows_to_table("تاریخچه بکاپ", backups)],
            "insights": ["نسخه پشتیبان فایل SQLite را در پوشه backups ذخیره می‌کند.", "برای بازیابی، کافی است فایل بکاپ را انتخاب کنید تا دیتابیس جایگزین شود."],
            "actions": ["backup", "restore"],
        }
