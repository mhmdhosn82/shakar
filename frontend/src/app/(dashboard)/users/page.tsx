"use client";

import { Plus, Shield, UserCog, UsersRound } from "lucide-react";

import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { DataTable, type ColumnDef } from "@/components/ui/DataTable";
import type { User } from "@/types";

const users: User[] = [
  { id: 1, fullName: "علی محمدی", username: "ali.manager", email: "ali@shakar.ir", phone: "09121234567", status: "active", createdAt: "2024-01-10T09:00:00Z", lastLoginAt: "1405/04/21 - 07:45", role: { id: 1, name: "مدیر کل", permissions: [] }, branch: { id: 1, name: "شعبه مرکزی", code: "BR-001", city: "تهران", address: "-", status: "active", createdAt: "2024-01-10T09:00:00Z" } },
  { id: 2, fullName: "مریم رضایی", username: "maryam.sales", email: "maryam@shakar.ir", phone: "09124445566", status: "active", createdAt: "2024-02-02T09:00:00Z", lastLoginAt: "1405/04/21 - 08:20", role: { id: 2, name: "سرپرست فروش", permissions: [] }, branch: { id: 2, name: "شعبه شرق", code: "BR-002", city: "تهران", address: "-", status: "active", createdAt: "2024-03-14T09:00:00Z" } },
  { id: 3, fullName: "حسین یوسفی", username: "hossein.inv", email: "hossein@shakar.ir", phone: "09127778899", status: "inactive", createdAt: "2024-01-20T09:00:00Z", lastLoginAt: "1405/04/17 - 11:30", role: { id: 3, name: "انباردار", permissions: [] }, branch: { id: 1, name: "شعبه مرکزی", code: "BR-001", city: "تهران", address: "-", status: "active", createdAt: "2024-01-10T09:00:00Z" } },
];

const columns: ColumnDef<User>[] = [
  { key: "fullName", title: "کاربر", render: (_, row) => <div><p className="font-semibold text-slate-900 dark:text-white">{row.fullName}</p><p className="text-xs text-slate-500">{row.username}</p></div> },
  { key: "role", title: "نقش", render: (_, row) => row.role?.name ?? "-" },
  { key: "branch", title: "شعبه", render: (_, row) => row.branch?.name ?? "-" },
  { key: "lastLoginAt", title: "آخرین ورود" },
  { key: "status", title: "وضعیت", render: (value) => <Badge variant={value === "active" ? "success" : "warning"}>{value === "active" ? "فعال" : "غیرفعال"}</Badge> },
];

export default function UsersPage() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between"><div><h1 className="text-2xl font-black text-slate-900 dark:text-white">مدیریت کاربران</h1><p className="mt-2 text-sm leading-7 text-slate-600 dark:text-slate-300">نقش‌ها، دسترسی‌ها و وضعیت فعالیت کاربران هر شعبه را با دقت سازمانی کنترل کنید.</p></div><Button leftIcon={<Plus className="h-4 w-4" />}>کاربر جدید</Button></div>
      <div className="grid gap-4 md:grid-cols-3">
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-primary/10 p-3 text-primary"><UsersRound className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">کاربران فعال</p><p className="text-2xl font-black text-slate-900 dark:text-white">۲ نفر</p></div></CardContent></Card>
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-sky-500/10 p-3 text-sky-600"><UserCog className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">نقش‌های تعریف‌شده</p><p className="text-2xl font-black text-slate-900 dark:text-white">۵ نقش</p></div></CardContent></Card>
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-emerald-500/10 p-3 text-emerald-600"><Shield className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">سطح انطباق امنیتی</p><p className="text-2xl font-black text-slate-900 dark:text-white">عالی</p></div></CardContent></Card>
      </div>
      <Card><CardHeader><CardTitle>لیست کاربران</CardTitle><CardDescription>کاربران فروش، انبار، حسابداری و مدیریت در این جدول قابل مشاهده هستند.</CardDescription></CardHeader><CardContent><DataTable columns={columns} data={users} caption="کاربران تعریف‌شده در سامانه" emptyTitle="کاربری ثبت نشده است" emptyDescription="بعد از ثبت اولین کاربر، اطلاعات او در این جدول نمایش داده خواهد شد." /></CardContent></Card>
    </div>
  );
}
