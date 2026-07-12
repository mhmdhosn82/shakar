from __future__ import annotations

from pathlib import Path

APP_NAME = "فروشگاه شاکار"
APP_VERSION = "2.0.0-desktop"
ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
BACKUP_DIR = ROOT_DIR / "backups"
EXPORT_DIR = ROOT_DIR / "exports"
DATABASE_PATH = DATA_DIR / "shakar_desktop.db"
WINDOW_MIN_SIZE = (1360, 860)

ROLE_PERMISSIONS: dict[str, set[str]] = {
    "super_admin": {"*"},
    "admin": {
        "dashboard",
        "users",
        "roles",
        "branches",
        "inventory",
        "catalog",
        "purchases",
        "sales",
        "installments",
        "customers",
        "suppliers",
        "payments",
        "accounting",
        "expenses",
        "service",
        "reports",
        "settings",
    },
    "manager": {
        "dashboard",
        "branches",
        "inventory",
        "catalog",
        "purchases",
        "sales",
        "installments",
        "customers",
        "suppliers",
        "payments",
        "expenses",
        "service",
        "reports",
    },
    "accountant": {
        "dashboard",
        "sales",
        "installments",
        "customers",
        "suppliers",
        "payments",
        "accounting",
        "expenses",
        "reports",
    },
    "cashier": {"dashboard", "sales", "installments", "customers", "payments"},
    "warehouse": {"dashboard", "inventory", "catalog", "purchases", "suppliers", "reports"},
}

MODULE_TITLES = {
    "dashboard": "داشبورد مدیریتی",
    "users": "کاربران و احراز هویت",
    "roles": "نقش‌ها و دسترسی‌ها",
    "branches": "شعب و انبارها",
    "inventory": "انبار و موجودی",
    "catalog": "کاتالوگ کالا و سازگاری",
    "purchases": "خرید و تامین",
    "sales": "فروش و اقساط",
    "installments": "اقساط و مطالبات",
    "customers": "مشتریان",
    "suppliers": "تامین‌کنندگان",
    "payments": "وجوه و صندوق‌ها",
    "accounting": "حسابداری",
    "expenses": "هزینه‌ها",
    "service": "مرجوعی، گارانتی و تعمیرات",
    "reports": "گزارش‌های مدیریتی و هوشمند",
    "settings": "تنظیمات و پشتیبان‌گیری",
}
