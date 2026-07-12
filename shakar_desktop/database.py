from __future__ import annotations

import json
import shutil
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path

from .config import BACKUP_DIR, DATA_DIR, DATABASE_PATH, EXPORT_DIR
from .security import hash_password

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS branches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    code TEXT NOT NULL UNIQUE,
    manager_name TEXT,
    city TEXT,
    address TEXT,
    phone TEXT,
    is_active INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS warehouses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    branch_id INTEGER NOT NULL REFERENCES branches(id),
    name TEXT NOT NULL,
    code TEXT NOT NULL UNIQUE,
    capacity INTEGER NOT NULL DEFAULT 0,
    notes TEXT
);
CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    level INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS role_permissions (
    role_id INTEGER NOT NULL REFERENCES roles(id),
    permission_id INTEGER NOT NULL REFERENCES permissions(id),
    PRIMARY KEY (role_id, permission_id)
);
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    role_id INTEGER NOT NULL REFERENCES roles(id),
    branch_id INTEGER NOT NULL REFERENCES branches(id),
    is_active INTEGER NOT NULL DEFAULT 1,
    is_super_admin INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    code TEXT NOT NULL UNIQUE,
    parent_id INTEGER REFERENCES categories(id)
);
CREATE TABLE IF NOT EXISTS brands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    code TEXT NOT NULL UNIQUE,
    country TEXT
);
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    product_type TEXT NOT NULL,
    category_id INTEGER REFERENCES categories(id),
    brand_id INTEGER REFERENCES brands(id),
    branch_id INTEGER NOT NULL REFERENCES branches(id),
    cost_price REAL NOT NULL,
    sale_price REAL NOT NULL,
    reorder_point INTEGER NOT NULL DEFAULT 0,
    stock_quantity INTEGER NOT NULL DEFAULT 0,
    imei_required INTEGER NOT NULL DEFAULT 0,
    compatible_devices TEXT NOT NULL DEFAULT '[]',
    cross_sell_skus TEXT NOT NULL DEFAULT '[]',
    bundle_offer TEXT,
    trend_score REAL NOT NULL DEFAULT 0,
    last_sold_at TEXT,
    is_active INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS imei_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL REFERENCES products(id),
    warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
    imei TEXT NOT NULL UNIQUE,
    serial_number TEXT,
    status TEXT NOT NULL,
    warranty_until TEXT
);
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    mobile TEXT NOT NULL,
    city TEXT,
    loyalty_tier TEXT,
    credit_limit REAL NOT NULL DEFAULT 0,
    balance REAL NOT NULL DEFAULT 0,
    notes TEXT
);
CREATE TABLE IF NOT EXISTS suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    contact_name TEXT,
    mobile TEXT,
    city TEXT,
    payables_balance REAL NOT NULL DEFAULT 0,
    rating REAL NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS purchases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_no TEXT NOT NULL UNIQUE,
    supplier_id INTEGER NOT NULL REFERENCES suppliers(id),
    branch_id INTEGER NOT NULL REFERENCES branches(id),
    warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
    purchased_at TEXT NOT NULL,
    total REAL NOT NULL,
    paid REAL NOT NULL,
    status TEXT NOT NULL,
    notes TEXT
);
CREATE TABLE IF NOT EXISTS purchase_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    purchase_id INTEGER NOT NULL REFERENCES purchases(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id),
    qty INTEGER NOT NULL,
    unit_cost REAL NOT NULL,
    line_total REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_no TEXT NOT NULL UNIQUE,
    customer_id INTEGER REFERENCES customers(id),
    branch_id INTEGER NOT NULL REFERENCES branches(id),
    salesperson_id INTEGER REFERENCES users(id),
    sold_at TEXT NOT NULL,
    total REAL NOT NULL,
    paid REAL NOT NULL,
    profit REAL NOT NULL,
    payment_type TEXT NOT NULL,
    status TEXT NOT NULL,
    notes TEXT
);
CREATE TABLE IF NOT EXISTS sale_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_id INTEGER NOT NULL REFERENCES sales(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id),
    qty INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    line_total REAL NOT NULL,
    imei_id INTEGER REFERENCES imei_items(id)
);
CREATE TABLE IF NOT EXISTS installment_plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_id INTEGER NOT NULL REFERENCES sales(id) ON DELETE CASCADE,
    down_payment REAL NOT NULL,
    installment_amount REAL NOT NULL,
    installment_count INTEGER NOT NULL,
    interest_rate REAL NOT NULL,
    remaining_amount REAL NOT NULL,
    status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS installment_schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_id INTEGER NOT NULL REFERENCES installment_plans(id) ON DELETE CASCADE,
    due_date TEXT NOT NULL,
    amount REAL NOT NULL,
    paid_amount REAL NOT NULL,
    status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS funds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    fund_type TEXT NOT NULL,
    balance REAL NOT NULL,
    branch_id INTEGER NOT NULL REFERENCES branches(id)
);
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_type TEXT NOT NULL,
    source_id INTEGER NOT NULL,
    direction TEXT NOT NULL,
    fund_id INTEGER NOT NULL REFERENCES funds(id),
    amount REAL NOT NULL,
    method TEXT NOT NULL,
    paid_at TEXT NOT NULL,
    note TEXT
);
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    account_type TEXT NOT NULL,
    balance REAL NOT NULL DEFAULT 0,
    parent_code TEXT
);
CREATE TABLE IF NOT EXISTS journal_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_no TEXT NOT NULL UNIQUE,
    branch_id INTEGER REFERENCES branches(id),
    entry_date TEXT NOT NULL,
    description TEXT,
    total_debit REAL NOT NULL,
    total_credit REAL NOT NULL,
    status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS journal_lines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_id INTEGER NOT NULL REFERENCES journal_entries(id) ON DELETE CASCADE,
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    debit REAL NOT NULL,
    credit REAL NOT NULL,
    description TEXT
);
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    branch_id INTEGER NOT NULL REFERENCES branches(id),
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    expense_date TEXT NOT NULL,
    paid_from_fund_id INTEGER NOT NULL REFERENCES funds(id),
    approved_by TEXT,
    notes TEXT
);
CREATE TABLE IF NOT EXISTS returns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    return_no TEXT NOT NULL UNIQUE,
    sale_id INTEGER REFERENCES sales(id),
    customer_id INTEGER REFERENCES customers(id),
    product_id INTEGER REFERENCES products(id),
    reason TEXT NOT NULL,
    status TEXT NOT NULL,
    amount REAL NOT NULL,
    opened_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS repairs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_no TEXT NOT NULL UNIQUE,
    customer_id INTEGER REFERENCES customers(id),
    device_model TEXT NOT NULL,
    imei_or_serial TEXT,
    issue_summary TEXT NOT NULL,
    estimated_cost REAL NOT NULL,
    status TEXT NOT NULL,
    received_at TEXT NOT NULL,
    technician TEXT,
    warranty_claim INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS backup_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    backup_path TEXT NOT NULL,
    created_at TEXT NOT NULL,
    created_by TEXT
);
CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    action TEXT NOT NULL,
    details TEXT,
    created_at TEXT NOT NULL
);
"""

ROLE_SEEDS = [
    ("super_admin", "مالک / کنترل کامل", 100),
    ("admin", "مدیریت ارشد فروشگاه", 90),
    ("manager", "مدیر عملیات و شعب", 70),
    ("accountant", "مالی و حسابداری", 60),
    ("cashier", "صندوقدار", 40),
    ("warehouse", "انباردار و تامین", 40),
]
PERMISSION_SEEDS = [
    ("dashboard", "داشبورد مدیریتی"), ("users", "کاربران"), ("roles", "نقش‌ها"), ("branches", "شعب"),
    ("inventory", "موجودی"), ("catalog", "کاتالوگ کالا"), ("purchases", "خرید"), ("sales", "فروش"),
    ("installments", "اقساط"), ("customers", "مشتریان"), ("suppliers", "تامین‌کنندگان"), ("payments", "وجوه"),
    ("accounting", "حسابداری"), ("expenses", "هزینه‌ها"), ("service", "مرجوعی و تعمیرات"),
    ("reports", "گزارش‌ها"), ("settings", "تنظیمات"),
]
ROLE_PERMISSION_MAP = {
    "super_admin": [code for code, _ in PERMISSION_SEEDS],
    "admin": [code for code, _ in PERMISSION_SEEDS],
    "manager": ["dashboard", "branches", "inventory", "catalog", "purchases", "sales", "installments", "customers", "suppliers", "payments", "expenses", "service", "reports"],
    "accountant": ["dashboard", "sales", "installments", "customers", "suppliers", "payments", "accounting", "expenses", "reports"],
    "cashier": ["dashboard", "sales", "installments", "customers", "payments"],
    "warehouse": ["dashboard", "inventory", "catalog", "purchases", "suppliers", "reports"],
}


def utcnow() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat(sep=" ")


@contextmanager
def db_connection(db_path: Path = DATABASE_PATH):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def initialize_database(db_path: Path = DATABASE_PATH) -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    with db_connection(db_path) as connection:
        connection.executescript(SCHEMA_SQL)
        if connection.execute("SELECT 1 FROM settings WHERE key='db_seeded'").fetchone() is None:
            seed_database(connection)
    return db_path


def _account_id_map(connection: sqlite3.Connection) -> dict[str, int]:
    return {row["code"]: row["id"] for row in connection.execute("SELECT id, code FROM accounts")}


def _insert_journal_entry(
    connection: sqlite3.Connection,
    entry_no: str,
    branch_id: int,
    description: str,
    lines: list[tuple[str, float, float, str]],
    entry_date: str,
) -> int:
    total_debit = round(sum(line[1] for line in lines), 2)
    total_credit = round(sum(line[2] for line in lines), 2)
    entry_id = connection.execute(
        "INSERT INTO journal_entries(entry_no, branch_id, entry_date, description, total_debit, total_credit, status) VALUES (?, ?, ?, ?, ?, ?, 'posted')",
        (entry_no, branch_id, entry_date, description, total_debit, total_credit),
    ).lastrowid
    account_ids = _account_id_map(connection)
    connection.executemany(
        "INSERT INTO journal_lines(entry_id, account_id, debit, credit, description) VALUES (?, ?, ?, ?, ?)",
        [(entry_id, account_ids[code], debit, credit, note) for code, debit, credit, note in lines],
    )
    for code, debit, credit, _ in lines:
        connection.execute(
            "UPDATE accounts SET balance = balance + ? - ? WHERE code = ?",
            (debit, credit, code),
        )
    return entry_id


def seed_database(connection: sqlite3.Connection) -> None:
    now = utcnow()
    connection.executemany("INSERT INTO roles(name, description, level) VALUES (?, ?, ?)", ROLE_SEEDS)
    connection.executemany("INSERT INTO permissions(code, title) VALUES (?, ?)", PERMISSION_SEEDS)
    role_ids = {row["name"]: row["id"] for row in connection.execute("SELECT id, name FROM roles")}
    permission_ids = {row["code"]: row["id"] for row in connection.execute("SELECT id, code FROM permissions")}
    connection.executemany(
        "INSERT INTO role_permissions(role_id, permission_id) VALUES (?, ?)",
        [(role_ids[role], permission_ids[code]) for role, codes in ROLE_PERMISSION_MAP.items() for code in codes],
    )

    branches = [
        ("شعبه مرکزی تهران", "THR-HQ", "محمد حسینی", "تهران", "خیابان جمهوری، پاساژ موبایل ایران", "021-66770011", 1),
        ("شعبه کرج", "KRJ-01", "الهام قاسمی", "کرج", "گوهردشت، مرکز خرید البرز", "026-34550022", 1),
    ]
    connection.executemany("INSERT INTO branches(name, code, manager_name, city, address, phone, is_active) VALUES (?, ?, ?, ?, ?, ?, ?)", branches)
    branch_ids = {row["code"]: row["id"] for row in connection.execute("SELECT id, code FROM branches")}

    warehouses = [
        (branch_ids["THR-HQ"], "انبار مرکزی", "WH-THR", 1200, "گوشی‌های رجیسترشده و کالای پرگردش"),
        (branch_ids["KRJ-01"], "انبار کرج", "WH-KRJ", 600, "اکسسوری و کالاهای آماده فروش"),
    ]
    connection.executemany("INSERT INTO warehouses(branch_id, name, code, capacity, notes) VALUES (?, ?, ?, ?, ?)", warehouses)
    warehouse_ids = {row["code"]: row["id"] for row in connection.execute("SELECT id, code FROM warehouses")}

    users = [
        ("admin", "admin@shakar.ir", "مدیر کل سیستم", hash_password("Admin@123456"), role_ids["super_admin"], branch_ids["THR-HQ"], 1, 1, now),
        ("manager", "manager@shakar.ir", "الهام مدیر", hash_password("Manager@123456"), role_ids["manager"], branch_ids["THR-HQ"], 1, 0, now),
        ("cashier", "cashier@shakar.ir", "حامد صندوق", hash_password("Cashier@123456"), role_ids["cashier"], branch_ids["KRJ-01"], 1, 0, now),
        ("accountant", "accountant@shakar.ir", "سمیه مالی", hash_password("Accountant@123456"), role_ids["accountant"], branch_ids["THR-HQ"], 1, 0, now),
    ]
    connection.executemany(
        "INSERT INTO users(username, email, full_name, password_hash, role_id, branch_id, is_active, is_super_admin, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        users,
    )
    user_ids = {row["username"]: row["id"] for row in connection.execute("SELECT id, username FROM users")}

    categories = [
        ("گوشی موبایل", "MOBILE", None),
        ("اکسسوری", "ACCESSORY", None),
        ("شارژر و کابل", "CHARGER", None),
        ("گارد و گلس", "PROTECT", None),
        ("صوتی", "AUDIO", None),
    ]
    connection.executemany("INSERT INTO categories(name, code, parent_id) VALUES (?, ?, ?)", categories)
    category_ids = {row["code"]: row["id"] for row in connection.execute("SELECT id, code FROM categories")}

    brands = [("Apple", "APPLE", "USA"), ("Samsung", "SAMSUNG", "Korea"), ("Xiaomi", "XIAOMI", "China"), ("Anker", "ANKER", "China"), ("Baseus", "BASEUS", "China"), ("Green Lion", "GREENLION", "UAE")]
    connection.executemany("INSERT INTO brands(name, code, country) VALUES (?, ?, ?)", brands)
    brand_ids = {row["code"]: row["id"] for row in connection.execute("SELECT id, code FROM brands")}

    now_dt = datetime.utcnow()
    products = [
        ("IP15P-256-BLK", "iPhone 15 Pro 256GB مشکی", "mobile", category_ids["MOBILE"], brand_ids["APPLE"], branch_ids["THR-HQ"], 66500000, 71200000, 2, 3, 1, json.dumps(["iPhone 15 Pro"]), json.dumps(["CASE-IP15P", "GLASS-IP15P", "CH-ANKER-20W"]), "باندل اپل پریمیوم", 94.0, (now_dt - timedelta(days=1)).isoformat(sep=" "), 1),
        ("S24-256-GRY", "Samsung Galaxy S24 256GB خاکستری", "mobile", category_ids["MOBILE"], brand_ids["SAMSUNG"], branch_ids["THR-HQ"], 41200000, 44900000, 2, 4, 1, json.dumps(["Galaxy S24"]), json.dumps(["CASE-S24", "GLASS-S24", "PB-10000"]), "باندل سامسونگ اسمارت", 88.0, (now_dt - timedelta(days=3)).isoformat(sep=" "), 1),
        ("RN13-256-BLU", "Redmi Note 13 256GB آبی", "mobile", category_ids["MOBILE"], brand_ids["XIAOMI"], branch_ids["KRJ-01"], 15500000, 17650000, 3, 7, 1, json.dumps(["Redmi Note 13"]), json.dumps(["CASE-RN13", "GLASS-RN13", "CABLE-C2C"]), "پک اقتصادی شیائومی", 82.0, (now_dt - timedelta(days=12)).isoformat(sep=" "), 1),
        ("CASE-IP15P", "قاب مگ‌سیف iPhone 15 Pro", "accessory", category_ids["PROTECT"], brand_ids["GREENLION"], branch_ids["THR-HQ"], 420000, 690000, 12, 9, 0, json.dumps(["iPhone 15 Pro"]), json.dumps(["GLASS-IP15P", "CH-ANKER-20W"]), "پک محافظ اپل", 76.0, (now_dt - timedelta(days=2)).isoformat(sep=" "), 1),
        ("GLASS-IP15P", "گلس سرامیکی iPhone 15 Pro", "accessory", category_ids["PROTECT"], brand_ids["GREENLION"], branch_ids["THR-HQ"], 180000, 320000, 15, 6, 0, json.dumps(["iPhone 15 Pro"]), json.dumps(["CASE-IP15P"]), "پک محافظ اپل", 85.0, (now_dt - timedelta(days=2)).isoformat(sep=" "), 1),
        ("CH-ANKER-20W", "شارژر 20 وات Anker", "accessory", category_ids["CHARGER"], brand_ids["ANKER"], branch_ids["THR-HQ"], 640000, 980000, 10, 5, 0, json.dumps(["iPhone", "Galaxy", "Redmi"]), json.dumps(["CABLE-C2C", "CASE-IP15P"]), "پک شارژ سریع", 91.0, (now_dt - timedelta(days=6)).isoformat(sep=" "), 1),
        ("PB-10000", "پاوربانک 10000 Baseus", "accessory", category_ids["ACCESSORY"], brand_ids["BASEUS"], branch_ids["KRJ-01"], 980000, 1420000, 8, 3, 0, json.dumps(["Universal"]), json.dumps(["CABLE-C2C"]), "پک سفر", 79.0, (now_dt - timedelta(days=40)).isoformat(sep=" "), 1),
        ("CABLE-C2C", "کابل تایپ‌سی به تایپ‌سی 1 متری", "accessory", category_ids["CHARGER"], brand_ids["BASEUS"], branch_ids["KRJ-01"], 140000, 280000, 20, 25, 0, json.dumps(["Galaxy", "Redmi", "Power Bank"]), json.dumps(["CH-ANKER-20W", "PB-10000"]), "پک شارژ سریع", 73.0, (now_dt - timedelta(days=4)).isoformat(sep=" "), 1),
        ("CASE-S24", "قاب ضدضربه Galaxy S24", "accessory", category_ids["PROTECT"], brand_ids["GREENLION"], branch_ids["THR-HQ"], 310000, 590000, 10, 11, 0, json.dumps(["Galaxy S24"]), json.dumps(["GLASS-S24"]), "پک محافظ سامسونگ", 70.0, (now_dt - timedelta(days=20)).isoformat(sep=" "), 1),
        ("GLASS-S24", "گلس UV Galaxy S24", "accessory", category_ids["PROTECT"], brand_ids["GREENLION"], branch_ids["THR-HQ"], 170000, 310000, 10, 13, 0, json.dumps(["Galaxy S24"]), json.dumps(["CASE-S24"]), "پک محافظ سامسونگ", 67.0, (now_dt - timedelta(days=25)).isoformat(sep=" "), 1),
        ("CASE-RN13", "قاب شفاف Redmi Note 13", "accessory", category_ids["PROTECT"], brand_ids["GREENLION"], branch_ids["KRJ-01"], 110000, 240000, 12, 14, 0, json.dumps(["Redmi Note 13"]), json.dumps(["GLASS-RN13"]), "پک اقتصادی شیائومی", 64.0, (now_dt - timedelta(days=15)).isoformat(sep=" "), 1),
        ("GLASS-RN13", "گلس فول Redmi Note 13", "accessory", category_ids["PROTECT"], brand_ids["GREENLION"], branch_ids["KRJ-01"], 90000, 170000, 12, 18, 0, json.dumps(["Redmi Note 13"]), json.dumps(["CASE-RN13"]), "پک اقتصادی شیائومی", 62.0, (now_dt - timedelta(days=15)).isoformat(sep=" "), 1),
    ]
    connection.executemany(
        "INSERT INTO products(sku, name, product_type, category_id, brand_id, branch_id, cost_price, sale_price, reorder_point, stock_quantity, imei_required, compatible_devices, cross_sell_skus, bundle_offer, trend_score, last_sold_at, is_active) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        products,
    )
    product_ids = {row["sku"]: row["id"] for row in connection.execute("SELECT id, sku FROM products")}

    imeis = [
        (product_ids["IP15P-256-BLK"], warehouse_ids["WH-THR"], "356789012345671", "APL-IP15P-01", "in_stock", (now_dt + timedelta(days=365)).isoformat(sep=" ")),
        (product_ids["IP15P-256-BLK"], warehouse_ids["WH-THR"], "356789012345689", "APL-IP15P-02", "reserved", (now_dt + timedelta(days=365)).isoformat(sep=" ")),
        (product_ids["IP15P-256-BLK"], warehouse_ids["WH-THR"], "356789012345697", "APL-IP15P-03", "sold", (now_dt + timedelta(days=365)).isoformat(sep=" ")),
        (product_ids["S24-256-GRY"], warehouse_ids["WH-THR"], "358123450987651", "SMS-S24-01", "in_stock", (now_dt + timedelta(days=365)).isoformat(sep=" ")),
        (product_ids["S24-256-GRY"], warehouse_ids["WH-THR"], "358123450987669", "SMS-S24-02", "in_stock", (now_dt + timedelta(days=365)).isoformat(sep=" ")),
        (product_ids["RN13-256-BLU"], warehouse_ids["WH-KRJ"], "861234567890125", "XMI-RN13-01", "in_stock", (now_dt + timedelta(days=365)).isoformat(sep=" ")),
        (product_ids["RN13-256-BLU"], warehouse_ids["WH-KRJ"], "861234567890133", "XMI-RN13-02", "sold", (now_dt + timedelta(days=365)).isoformat(sep=" ")),
    ]
    connection.executemany("INSERT INTO imei_items(product_id, warehouse_id, imei, serial_number, status, warranty_until) VALUES (?, ?, ?, ?, ?, ?)", imeis)

    customers = [
        ("شرکت پارس ارتباط", "09121234567", "تهران", "طلایی", 120000000, 18500000, "خریدهای عمده و سفارش‌های سازمانی"),
        ("مهدی جلالی", "09123334455", "کرج", "نقره‌ای", 45000000, 9600000, "مشتری اقساطی گوشی سامسونگ"),
        ("فاطمه زمانی", "09351234567", "تهران", "برنزی", 18000000, 0, "خریدار اکسسوری‌های اپل"),
        ("سجاد پورموسوی", "09901112233", "شهریار", "جدید", 15000000, 0, "درخواست تعمیر و گارانتی"),
    ]
    connection.executemany("INSERT INTO customers(name, mobile, city, loyalty_tier, credit_limit, balance, notes) VALUES (?, ?, ?, ?, ?, ?, ?)", customers)
    customer_ids = {row["name"]: row["id"] for row in connection.execute("SELECT id, name FROM customers")}

    suppliers = [
        ("توسعه همراه ایرانیان", "علی مرادی", "02188776655", "تهران", 74000000, 4.7),
        ("آریا اکسسوری", "ندا توکلی", "02144112233", "تهران", 18200000, 4.4),
        ("دیجیتال کرج", "رضا فراهانی", "02633445566", "کرج", 12600000, 4.1),
    ]
    connection.executemany("INSERT INTO suppliers(name, contact_name, mobile, city, payables_balance, rating) VALUES (?, ?, ?, ?, ?, ?)", suppliers)
    supplier_ids = {row["name"]: row["id"] for row in connection.execute("SELECT id, name FROM suppliers")}

    funds = [
        ("صندوق تهران", "cash", 228500000, branch_ids["THR-HQ"]),
        ("بانک ملت تهران", "bank", 362000000, branch_ids["THR-HQ"]),
        ("صندوق کرج", "cash", 94500000, branch_ids["KRJ-01"]),
    ]
    connection.executemany("INSERT INTO funds(name, fund_type, balance, branch_id) VALUES (?, ?, ?, ?)", funds)
    fund_ids = {row["name"]: row["id"] for row in connection.execute("SELECT id, name FROM funds")}

    purchases = [
        ("PUR-1403-101", supplier_ids["توسعه همراه ایرانیان"], branch_ids["THR-HQ"], warehouse_ids["WH-THR"], (now_dt - timedelta(days=18)).isoformat(sep=" "), 256600000, 160000000, "approved", "خرید محموله گوشی و شارژر سریع"),
        ("PUR-1403-102", supplier_ids["آریا اکسسوری"], branch_ids["KRJ-01"], warehouse_ids["WH-KRJ"], (now_dt - timedelta(days=10)).isoformat(sep=" "), 17200000, 12000000, "approved", "شارژ موجودی گلس و قاب"),
    ]
    connection.executemany("INSERT INTO purchases(invoice_no, supplier_id, branch_id, warehouse_id, purchased_at, total, paid, status, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", purchases)
    purchase_ids = {row["invoice_no"]: row["id"] for row in connection.execute("SELECT id, invoice_no FROM purchases")}
    purchase_items = [
        (purchase_ids["PUR-1403-101"], product_ids["IP15P-256-BLK"], 2, 66500000, 133000000),
        (purchase_ids["PUR-1403-101"], product_ids["S24-256-GRY"], 3, 41200000, 123600000),
        (purchase_ids["PUR-1403-102"], product_ids["CASE-RN13"], 40, 110000, 4400000),
        (purchase_ids["PUR-1403-102"], product_ids["GLASS-RN13"], 60, 90000, 5400000),
        (purchase_ids["PUR-1403-102"], product_ids["CABLE-C2C"], 30, 140000, 4200000),
    ]
    connection.executemany("INSERT INTO purchase_items(purchase_id, product_id, qty, unit_cost, line_total) VALUES (?, ?, ?, ?, ?)", purchase_items)

    sales = [
        ("SAL-1403-5001", customer_ids["شرکت پارس ارتباط"], branch_ids["THR-HQ"], user_ids["admin"], (now_dt - timedelta(days=14)).isoformat(sep=" "), 74000000, 74000000, 4700000, "cash", "confirmed", "فروش شرکتی آیفون با باندل محافظ"),
        ("SAL-1403-5002", customer_ids["مهدی جلالی"], branch_ids["THR-HQ"], user_ids["manager"], (now_dt - timedelta(days=9)).isoformat(sep=" "), 45800000, 18000000, 3900000, "installment", "confirmed", "فروش اقساطی سامسونگ با پیش‌پرداخت"),
        ("SAL-1403-5003", customer_ids["فاطمه زمانی"], branch_ids["KRJ-01"], user_ids["cashier"], (now_dt - timedelta(days=4)).isoformat(sep=" "), 1660000, 1660000, 540000, "cash", "confirmed", "اکسسوری‌های اپل"),
        ("SAL-1403-5004", customer_ids["شرکت پارس ارتباط"], branch_ids["KRJ-01"], user_ids["cashier"], (now_dt - timedelta(days=2)).isoformat(sep=" "), 2840000, 2840000, 1320000, "cash", "confirmed", "فروش عمده پاوربانک و کابل"),
    ]
    connection.executemany("INSERT INTO sales(invoice_no, customer_id, branch_id, salesperson_id, sold_at, total, paid, profit, payment_type, status, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", sales)
    sale_ids = {row["invoice_no"]: row["id"] for row in connection.execute("SELECT id, invoice_no FROM sales")}
    imei_ids = {row["imei"]: row["id"] for row in connection.execute("SELECT id, imei FROM imei_items")}
    sale_items = [
        (sale_ids["SAL-1403-5001"], product_ids["IP15P-256-BLK"], 1, 71200000, 71200000, imei_ids["356789012345697"]),
        (sale_ids["SAL-1403-5001"], product_ids["CASE-IP15P"], 2, 690000, 1380000, None),
        (sale_ids["SAL-1403-5001"], product_ids["GLASS-IP15P"], 2, 320000, 640000, None),
        (sale_ids["SAL-1403-5002"], product_ids["S24-256-GRY"], 1, 44900000, 44900000, None),
        (sale_ids["SAL-1403-5002"], product_ids["CASE-S24"], 1, 590000, 590000, None),
        (sale_ids["SAL-1403-5002"], product_ids["GLASS-S24"], 1, 310000, 310000, None),
        (sale_ids["SAL-1403-5003"], product_ids["CASE-IP15P"], 1, 690000, 690000, None),
        (sale_ids["SAL-1403-5003"], product_ids["CH-ANKER-20W"], 1, 970000, 970000, None),
        (sale_ids["SAL-1403-5004"], product_ids["PB-10000"], 1, 1420000, 1420000, None),
        (sale_ids["SAL-1403-5004"], product_ids["CABLE-C2C"], 5, 284000, 1420000, None),
    ]
    connection.executemany("INSERT INTO sale_items(sale_id, product_id, qty, unit_price, line_total, imei_id) VALUES (?, ?, ?, ?, ?, ?)", sale_items)

    installment_plan_id = connection.execute(
        "INSERT INTO installment_plans(sale_id, down_payment, installment_amount, installment_count, interest_rate, remaining_amount, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (sale_ids["SAL-1403-5002"], 18000000, 9300000, 3, 2.5, 27900000, "active"),
    ).lastrowid
    for offset, status, paid in [(10, "paid", 9300000), (40, "overdue", 0), (70, "pending", 0)]:
        connection.execute(
            "INSERT INTO installment_schedules(plan_id, due_date, amount, paid_amount, status) VALUES (?, ?, ?, ?, ?)",
            (installment_plan_id, (now_dt - timedelta(days=offset)).isoformat(sep=" "), 9300000, paid, status),
        )

    payments = [
        ("sale", sale_ids["SAL-1403-5001"], "in", fund_ids["صندوق تهران"], 74000000, "cash", (now_dt - timedelta(days=14)).isoformat(sep=" "), "وصول کامل فروش"),
        ("sale", sale_ids["SAL-1403-5002"], "in", fund_ids["صندوق تهران"], 18000000, "cash", (now_dt - timedelta(days=9)).isoformat(sep=" "), "پیش‌پرداخت فروش اقساطی"),
        ("sale", sale_ids["SAL-1403-5003"], "in", fund_ids["صندوق کرج"], 1660000, "cash", (now_dt - timedelta(days=4)).isoformat(sep=" "), "وصول فروش اکسسوری"),
        ("sale", sale_ids["SAL-1403-5004"], "in", fund_ids["صندوق کرج"], 2840000, "card", (now_dt - timedelta(days=2)).isoformat(sep=" "), "وصول فروش سازمانی"),
        ("purchase", purchase_ids["PUR-1403-101"], "out", fund_ids["بانک ملت تهران"], 160000000, "bank_transfer", (now_dt - timedelta(days=18)).isoformat(sep=" "), "پرداخت به تامین‌کننده"),
        ("purchase", purchase_ids["PUR-1403-102"], "out", fund_ids["صندوق کرج"], 12000000, "cash", (now_dt - timedelta(days=10)).isoformat(sep=" "), "پرداخت بخشی خرید"),
    ]
    connection.executemany("INSERT INTO payments(source_type, source_id, direction, fund_id, amount, method, paid_at, note) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", payments)

    accounts = [
        ("1000", "صندوق نقد", "asset", 0, None),
        ("1100", "بانک", "asset", 0, None),
        ("1200", "حساب‌های دریافتنی", "asset", 0, None),
        ("1300", "موجودی کالا", "asset", 0, None),
        ("2000", "حساب‌های پرداختنی", "liability", 0, None),
        ("3000", "سرمایه", "equity", 0, None),
        ("4000", "درآمد فروش", "income", 0, None),
        ("5000", "بهای تمام‌شده کالای فروش‌رفته", "expense", 0, None),
        ("6100", "هزینه‌های اداری", "expense", 0, None),
    ]
    connection.executemany("INSERT INTO accounts(code, name, account_type, balance, parent_code) VALUES (?, ?, ?, ?, ?)", accounts)

    _insert_journal_entry(connection, "JE-OPEN-01", branch_ids["THR-HQ"], "سرمایه‌گذاری اولیه مالک", [("1000", 180000000, 0, "ورود نقد"), ("1100", 280000000, 0, "ورود بانک"), ("3000", 0, 460000000, "سرمایه مالک")], (now_dt - timedelta(days=30)).isoformat(sep=" "))
    _insert_journal_entry(connection, "JE-PUR-101", branch_ids["THR-HQ"], "خرید موجودی اصلی", [("1300", 256600000, 0, "خرید کالا"), ("1100", 0, 160000000, "پرداخت بانک"), ("2000", 0, 96600000, "بدهی به تامین‌کننده")], (now_dt - timedelta(days=18)).isoformat(sep=" "))
    _insert_journal_entry(connection, "JE-SAL-5001", branch_ids["THR-HQ"], "فروش نقدی آیفون", [("1000", 74000000, 0, "دریافت نقد"), ("4000", 0, 74000000, "درآمد فروش"), ("5000", 69300000, 0, "بهای تمام‌شده"), ("1300", 0, 69300000, "کاهش موجودی")], (now_dt - timedelta(days=14)).isoformat(sep=" "))
    _insert_journal_entry(connection, "JE-SAL-5002", branch_ids["THR-HQ"], "فروش اقساطی سامسونگ", [("1000", 18000000, 0, "پیش‌پرداخت"), ("1200", 27900000, 0, "مطالبات اقساطی"), ("4000", 0, 45900000, "درآمد فروش"), ("5000", 41510000, 0, "بهای تمام‌شده"), ("1300", 0, 41510000, "کاهش موجودی")], (now_dt - timedelta(days=9)).isoformat(sep=" "))

    expenses = [
        ("تبلیغات اینستاگرامی", branch_ids["THR-HQ"], "بازاریابی", 3500000, (now_dt - timedelta(days=6)).isoformat(sep=" "), fund_ids["بانک ملت تهران"], "مدیر کل سیستم", "کمپین فروش آیفون و اکسسوری"),
        ("هزینه سرویس پیک", branch_ids["KRJ-01"], "عملیات", 850000, (now_dt - timedelta(days=3)).isoformat(sep=" "), fund_ids["صندوق کرج"], "الهام مدیر", "ارسال سفارش سازمانی"),
    ]
    connection.executemany("INSERT INTO expenses(title, branch_id, category, amount, expense_date, paid_from_fund_id, approved_by, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", expenses)
    _insert_journal_entry(connection, "JE-EXP-01", branch_ids["THR-HQ"], "هزینه تبلیغات", [("6100", 3500000, 0, "هزینه تبلیغات"), ("1100", 0, 3500000, "پرداخت از بانک")], (now_dt - timedelta(days=6)).isoformat(sep=" "))

    returns = [
        ("RET-1403-201", sale_ids["SAL-1403-5003"], customer_ids["فاطمه زمانی"], product_ids["CH-ANKER-20W"], "خرابی آداپتور", "approved", 970000, (now_dt - timedelta(days=1)).isoformat(sep=" ")),
    ]
    connection.executemany("INSERT INTO returns(return_no, sale_id, customer_id, product_id, reason, status, amount, opened_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", returns)

    repairs = [
        ("REP-1403-301", customer_ids["سجاد پورموسوی"], "iPhone 13", "352000111222333", "تعویض فلت شارژ", 2600000, "in_progress", (now_dt - timedelta(days=2)).isoformat(sep=" "), "تکنسین رفیعی", 0),
        ("REP-1403-302", customer_ids["شرکت پارس ارتباط"], "Samsung A54", "359990001112223", "بررسی گارانتی باتری", 0, "awaiting_parts", (now_dt - timedelta(days=1)).isoformat(sep=" "), "تکنسین شریفی", 1),
    ]
    connection.executemany("INSERT INTO repairs(ticket_no, customer_id, device_model, imei_or_serial, issue_summary, estimated_cost, status, received_at, technician, warranty_claim) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", repairs)

    settings = [
        ("app_theme", "midnight", now),
        ("currency", "IRR", now),
        ("rtl", "true", now),
        ("backup_policy", "روزانه + قبل از تغییرات حساس", now),
        ("smart_reorder_days", "14", now),
        ("db_seeded", "true", now),
    ]
    connection.executemany("INSERT INTO settings(key, value, updated_at) VALUES (?, ?, ?)", settings)
    connection.execute("INSERT INTO audit_logs(username, action, details, created_at) VALUES (?, ?, ?, ?)", ("system", "seed", "داده‌های دموی فروشگاه ایجاد شد", now))


def create_backup_copy(db_path: Path = DATABASE_PATH, *, actor: str = "system") -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    target = BACKUP_DIR / f"shakar-backup-{timestamp}.db"
    shutil.copy2(db_path, target)
    with db_connection(db_path) as connection:
        connection.execute("INSERT INTO backup_history(backup_path, created_at, created_by) VALUES (?, ?, ?)", (str(target), utcnow(), actor))
    return target


def restore_backup_copy(source: Path, db_path: Path = DATABASE_PATH) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, db_path)
