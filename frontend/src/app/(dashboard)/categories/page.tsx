"use client";

import { FolderTree, Layers2, Plus, Tag } from "lucide-react";

import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { DataTable, type ColumnDef } from "@/components/ui/DataTable";
import type { Category } from "@/types";

const categories: Category[] = [
  { id: 1, name: "شارژر", slug: "charger", description: "انواع شارژر و آداپتور", status: "active", productsCount: 82 },
  { id: 2, name: "محافظ صفحه", slug: "screen-protector", description: "گلس و محافظ‌های صفحه", status: "active", productsCount: 146 },
  { id: 3, name: "هندزفری", slug: "headset", description: "هندزفری سیمی و بی‌سیم", status: "active", productsCount: 54 },
  { id: 4, name: "کابل", slug: "cable", description: "کابل‌های شارژ و انتقال دیتا", status: "inactive", productsCount: 39 },
];

const columns: ColumnDef<Category>[] = [
  { key: "name", title: "نام دسته‌بندی" },
  { key: "description", title: "توضیحات" },
  { key: "productsCount", title: "تعداد کالاها" },
  { key: "status", title: "وضعیت", render: (value) => <Badge variant={value === "active" ? "success" : "warning"}>{value === "active" ? "فعال" : "غیرفعال"}</Badge> },
];

export default function CategoriesPage() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between"><div><h1 className="text-2xl font-black text-slate-900 dark:text-white">مدیریت دسته‌بندی‌ها</h1><p className="mt-2 text-sm leading-7 text-slate-600 dark:text-slate-300">ساختار دسته‌بندی محصولات را به‌صورت درختی و حرفه‌ای برای جستجو و گزارش‌گیری بهتر مدیریت کنید.</p></div><Button leftIcon={<Plus className="h-4 w-4" />}>دسته‌بندی جدید</Button></div>
      <div className="grid gap-4 md:grid-cols-3">
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-primary/10 p-3 text-primary"><FolderTree className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">کل دسته‌بندی‌ها</p><p className="text-2xl font-black text-slate-900 dark:text-white">۴ دسته</p></div></CardContent></Card>
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-emerald-500/10 p-3 text-emerald-600"><Layers2 className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">ساختار فعال</p><p className="text-2xl font-black text-slate-900 dark:text-white">۳ شاخه</p></div></CardContent></Card>
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-sky-500/10 p-3 text-sky-600"><Tag className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">قابل استفاده در POS</p><p className="text-2xl font-black text-slate-900 dark:text-white">۱۰۰٪</p></div></CardContent></Card>
      </div>
      <Card><CardHeader><CardTitle>فهرست دسته‌بندی‌ها</CardTitle><CardDescription>دسته‌های اصلی و فرعی کالاها در این بخش قابل مدیریت هستند.</CardDescription></CardHeader><CardContent><DataTable columns={columns} data={categories} caption="ساختار دسته‌بندی فروشگاه" emptyTitle="دسته‌بندی ثبت نشده است" emptyDescription="پس از ایجاد دسته‌بندی جدید، لیست این بخش تکمیل می‌شود." /></CardContent></Card>
    </div>
  );
}
