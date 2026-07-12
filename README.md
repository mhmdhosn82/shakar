# فروشگاه شاکار — Shakar Store Management System

<div align="center">

## 🏪 فروشگاه شاکار
### سیستم جامع مدیریت فروشگاه موبایل و اکسسوری

**نسخه ۱.۰.۰** | توسعه‌دهنده: محمدحسین آقازاده

[![Python](https://img.shields.io/badge/Python-3.11%20recommended-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green.svg)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org)
[![SQLite](https://img.shields.io/badge/SQLite-Dev%20Default-003b57.svg)](https://sqlite.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Production-blue.svg)](https://postgresql.org)

</div>

---

## معرفی سیستم

**فروشگاه شاکار** یک سیستم جامع مدیریت فروشگاهی، حسابداری و انبارداری برای فروشگاه‌های موبایل و اکسسوری است. این پروژه با FastAPI در بک‌اند و Next.js در فرانت‌اند ساخته شده و به‌صورت ماژولار طراحی شده تا برای توسعه نسخه‌های حرفه‌ای‌تر آماده باشد.

### ویژگی‌های کلیدی

- 🏬 **چند شعبه‌ای** — مدیریت چندین شعبه با گزارش‌های تجمیعی
- 📱 **ردیابی IMEI** — ثبت و پیگیری هر دستگاه با شماره IMEI
- 💰 **فروش اقساطی** — مدیریت اقساط، سررسیدها و یادآوری‌ها
- 📦 **انبارداری دقیق** — کنترل موجودی با هشدار کمبود
- 📊 **حسابداری یکپارچه** — کدینگ حساب‌ها و اسناد مالی
- 👥 **CRM مشتریان** — پرونده مشتری و تاریخچه خرید
- 🔐 **کنترل دسترسی** — نقش‌ها و مجوزهای سطح‌بندی شده
- 💾 **بکاپ خودکار** — پشتیبان‌گیری امن با رمزنگاری

---

## معماری

```
Frontend (Next.js 14 + TypeScript + Tailwind CSS RTL)
        ↕
Backend (FastAPI + Python + SQLAlchemy 2.x async)
        ↕
Database (SQLite for local dev / PostgreSQL for production) + Cache (Redis optional)
```

### Technology Stack

| Layer       | Technology                              |
|-------------|------------------------------------------|
| Backend     | Python 3.11 recommended, FastAPI 0.111   |
| ORM         | SQLAlchemy 2.x (async)                   |
| Migrations  | Alembic                                  |
| Database    | SQLite (dev), PostgreSQL (production)    |
| Cache       | Redis (optional)                         |
| Frontend    | Next.js 14, TypeScript, Tailwind         |
| Auth        | JWT (python-jose) + bcrypt               |
| Container   | Docker + Docker Compose                  |

---

## ماژول‌ها

| ماژول                | وضعیت |
|---------------------|--------|
| احراز هویت          | ✅     |
| مدیریت کاربران      | ✅     |
| مدیریت شعبات        | ✅     |
| کالا و دسته‌بندی    | ✅     |
| انبارداری + IMEI    | ✅     |
| مشتریان و تامین‌کنندگان | ✅  |
| فروش (نقدی/اقساطی)  | ✅     |
| خرید                | ✅     |
| حسابداری            | ✅     |
| بکاپ و ریستور       | ✅     |
| آدیت لاگ            | ✅     |

---

## پیش‌نیازها

### مسیر پیشنهادی برای توسعه محلی
- Python **3.11** یا **3.12**
- Node.js 20+

### گزینه‌های اجرا
- **بدون Docker و بدون PostgreSQL برای شروع سریع:** SQLite پیش‌فرض است.
- **برای محیط production-like:** PostgreSQL و Docker Compose.

> توجه: Python 3.13 ممکن است با بعضی وابستگی‌های باینری مثل `asyncpg` و `pydantic-core` روی برخی سیستم‌ها دردسر ایجاد کند. برای اجرای مطمئن، Python 3.11 توصیه می‌شود.

---

## نصب و راه‌اندازی

### توسعه سریع بدون Docker (توصیه‌شده برای ویندوز)

#### Backend
```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# ساخت فایل تنظیمات
copy .env.example .env
# یا در Linux/macOS:
# cp .env.example .env

alembic upgrade head
python -m app.db.init_db
uvicorn app.main:app --reload --port 8000
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

### دسترسی

| سرویس        | آدرس                      |
|-------------|---------------------------|
| پنل مدیریت  | http://localhost:3000     |
| API Backend | http://localhost:8000     |
| API Docs    | http://localhost:8000/docs |

**اطلاعات ورود پیش‌فرض:** `admin@shakar.ir` / `Admin@123456`

---

## اجرای PostgreSQL به‌جای SQLite

اگر خواستی به‌جای SQLite از PostgreSQL استفاده کنی، فایل `backend/.env` را تغییر بده:

```env
DATABASE_URL=postgresql+asyncpg://shakar:shakar@localhost:5432/shakar_db
```

در این حالت باید PostgreSQL نصب و در حال اجرا باشد.

---

## نصب با Docker

```bash
git clone https://github.com/mhmdhosn82/shakar.git
cd shakar
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local
docker compose up -d
docker compose exec backend alembic upgrade head
docker compose exec backend python -m app.db.init_db
```

---

## ساختار پروژه

```
shakar/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/  # API route handlers
│   │   ├── core/              # Config, security, DB, logging
│   │   ├── models/            # SQLAlchemy ORM models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   └── db/                # DB init and seeding
│   ├── migrations/            # Alembic migrations
│   ├── tests/
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── app/               # Next.js App Router pages
│   │   ├── components/        # UI components
│   │   ├── lib/               # API client, utilities
│   │   └── types/             # TypeScript types
│   └── package.json
├── docker-compose.yml
└── README.md
```

---

## بکاپ و ریستور

### PostgreSQL
```bash
# بکاپ
docker compose exec db pg_dump -U shakar shakar_db | gzip > backup.sql.gz

# ریستور
docker compose exec -T db psql -U shakar shakar_db < backup.sql
```

### SQLite
```bash
# بکاپ فایل توسعه
copy backend\shakar.db backend\shakar-backup.db
```

---

## لایسنس

تمامی حقوق محفوظ است. © ۱۴۰۳ فروشگاه شاکار  
توسعه‌دهنده: محمدحسین آقازاده
