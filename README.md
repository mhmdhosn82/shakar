# فروشگاه شاکار — Shakar Store Management System

<div align="center">

## 🏪 فروشگاه شاکار
### سیستم جامع مدیریت فروشگاه موبایل و اکسسوری

**نسخه ۱.۰.۰** | توسعه‌دهنده: محمدحسین آقازاده

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green.svg)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://docker.com)

</div>

---

## معرفی سیستم

**فروشگاه شاکار** یک سیستم جامع مدیریت فروشگاهی، حسابداری و انبارداری است که برای فروشگاه‌های موبایل و اکسسوری طراحی شده است.

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
Backend (FastAPI + Python 3.11 + SQLAlchemy 2.x async)
        ↕
Database (PostgreSQL 16) + Cache (Redis 7)
```

### Technology Stack

| Layer       | Technology                          |
|-------------|-------------------------------------|
| Backend     | Python 3.11, FastAPI 0.111          |
| ORM         | SQLAlchemy 2.x (async)              |
| Migrations  | Alembic                             |
| Database    | PostgreSQL 16                       |
| Cache       | Redis 7                             |
| Frontend    | Next.js 14, TypeScript, Tailwind    |
| Auth        | JWT (python-jose) + bcrypt          |
| Container   | Docker + Docker Compose             |

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

- Docker 24+ و Docker Compose 2.x
- یا: Python 3.11+ و Node.js 20+ و PostgreSQL 15+

---

## نصب و راه‌اندازی

### با Docker (توصیه شده)

```bash
# کلون مخزن
git clone https://github.com/mhmdhosn82/shakar.git
cd shakar

# تنظیم متغیرهای محیطی
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local

# اجرا
docker compose up -d

# اجرای migrations
docker compose exec backend alembic upgrade head

# ایجاد داده‌های اولیه
docker compose exec backend python -m app.db.init_db
```

### دسترسی

| سرویس        | آدرس                          |
|-------------|-------------------------------|
| پنل مدیریت  | http://localhost:3000          |
| API Backend | http://localhost:8000          |
| API Docs    | http://localhost:8000/docs     |

**اطلاعات ورود پیش‌فرض:** `admin@shakar.ir` / `Admin@123456`

---

## توسعه بدون Docker

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python -m app.db.init_db
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
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

```bash
# بکاپ
docker compose exec db pg_dump -U shakar shakar_db | gzip > backup.sql.gz

# ریستور
docker compose exec -T db psql -U shakar shakar_db < backup.sql
```

---

## لایسنس

تمامی حقوق محفوظ است. © ۱۴۰۳ فروشگاه شاکار  
توسعه‌دهنده: محمدحسین آقازاده
