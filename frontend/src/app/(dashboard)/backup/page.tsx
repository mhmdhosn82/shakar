"use client";

import { DatabaseBackup, Download, HardDriveUpload, ShieldCheck } from "lucide-react";

import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { DataTable, type ColumnDef } from "@/components/ui/DataTable";

type BackupRecord = { id: number; name: string; createdAt: string; size: string; storage: string; status: "completed" | "running" };
const backups: BackupRecord[] = [
  { id: 1, name: "backup-full-1405-04-21.sql.gz", createdAt: "امروز، 03:00", size: "185 MB", storage: "سرور پشتیبان داخلی", status: "completed" },
  { id: 2, name: "backup-media-1405-04-20.tar.gz", createdAt: "دیروز، 03:15", size: "620 MB", storage: "فضای آرشیو سرد", status: "completed" },
  { id: 3, name: "backup-incremental-1405-04-21-10.sql.gz", createdAt: "امروز، 10:00", size: "24 MB", storage: "صف همگام‌سازی", status: "running" },
];
const columns: ColumnDef<BackupRecord>[] = [
  { key: "name", title: "نام فایل" },
  { key: "createdAt", title: "زمان ایجاد" },
  { key: "size", title: "حجم" },
  { key: "storage", title: "محل نگهداری" },
  { key: "status", title: "وضعیت", render: (value) => <Badge variant={value === "completed" ? "success" : "info"}>{value === "completed" ? "تکمیل‌شده" : "در حال اجرا"}</Badge> },
];

export default function BackupPage() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between"><div><h1 className="text-2xl font-black text-slate-900 dark:text-white">پشتیبان‌گیری و بازیابی</h1><p className="mt-2 text-sm leading-7 text-slate-600 dark:text-slate-300">مدیریت نسخه‌های پشتیبان پایگاه داده و فایل‌ها برای تضمین تداوم کسب‌وکار و امنیت اطلاعات.</p></div><div className="flex gap-3"><Button variant="secondary" leftIcon={<HardDriveUpload className="h-4 w-4" />}>بازیابی نسخه</Button><Button leftIcon={<DatabaseBackup className="h-4 w-4" />}>ایجاد پشتیبان جدید</Button></div></div>
      <div className="grid gap-4 md:grid-cols-4">
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-primary/10 p-3 text-primary"><DatabaseBackup className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">آخرین پشتیبان کامل</p><p className="text-2xl font-black text-slate-900 dark:text-white">امروز 03:00</p></div></CardContent></Card>
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-sky-500/10 p-3 text-sky-600"><Download className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">نسخه‌های ذخیره‌شده</p><p className="text-2xl font-black text-slate-900 dark:text-white">۳۲ فایل</p></div></CardContent></Card>
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-emerald-500/10 p-3 text-emerald-600"><ShieldCheck className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">وضعیت مانیتورینگ</p><p className="text-2xl font-black text-slate-900 dark:text-white">پایدار</p></div></CardContent></Card>
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-amber-500/10 p-3 text-amber-600"><HardDriveUpload className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">چرخه نگهداری</p><p className="text-2xl font-black text-slate-900 dark:text-white">۳۰ روز</p></div></CardContent></Card>
      </div>
      <Card><CardHeader><CardTitle>تاریخچه نسخه‌های پشتیبان</CardTitle><CardDescription>تمامی نسخه‌های کامل و افزایشی برای بازیابی سریع در دسترس هستند.</CardDescription></CardHeader><CardContent><DataTable columns={columns} data={backups} caption="نسخه‌های پشتیبان موجود" emptyTitle="نسخه پشتیبانی وجود ندارد" emptyDescription="پس از اجرای اولین فرایند پشتیبان‌گیری، سوابق آن در این بخش ثبت می‌شود." /></CardContent></Card>
    </div>
  );
}
