"use client";

import { CreditCard, Plus, UserRound, WalletCards } from "lucide-react";

import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { DataTable, type ColumnDef } from "@/components/ui/DataTable";
import { formatCurrency } from "@/lib/utils";
import type { Customer } from "@/types";

const customers: Customer[] = [
  { id: 1, fullName: "رضا اکبری", phone: "09121231234", email: "reza@example.com", branchId: 1, status: "active", balance: 2400000, loyaltyLevel: "طلایی", lastPurchaseAt: "1405/04/21", createdAt: "2024-01-04T09:00:00Z" },
  { id: 2, fullName: "سمیرا حسینی", phone: "09129876543", email: "samira@example.com", branchId: 2, status: "active", balance: 0, loyaltyLevel: "نقره‌ای", lastPurchaseAt: "1405/04/20", createdAt: "2024-03-22T09:00:00Z" },
  { id: 3, fullName: "مهدی جلالی", phone: "09127770011", email: "mehdi@example.com", branchId: 1, status: "inactive", balance: 870000, loyaltyLevel: "عادی", lastPurchaseAt: "1405/04/12", createdAt: "2024-02-11T09:00:00Z" },
];

const columns: ColumnDef<Customer>[] = [
  { key: "fullName", title: "مشتری", render: (_, row) => <div><p className="font-semibold text-slate-900 dark:text-white">{row.fullName}</p><p className="text-xs text-slate-500">{row.phone}</p></div> },
  { key: "loyaltyLevel", title: "سطح باشگاه" },
  { key: "balance", title: "مانده حساب", render: (value) => formatCurrency(Number(value)) },
  { key: "lastPurchaseAt", title: "آخرین خرید" },
  { key: "status", title: "وضعیت", render: (value) => <Badge variant={value === "active" ? "success" : "outline"}>{value === "active" ? "فعال" : "غیرفعال"}</Badge> },
];

export default function CustomersPage() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between"><div><h1 className="text-2xl font-black text-slate-900 dark:text-white">مدیریت مشتریان</h1><p className="mt-2 text-sm leading-7 text-slate-600 dark:text-slate-300">اطلاعات مشتریان، مانده حساب، باشگاه وفاداری و الگوی خرید را برای فروش هدفمند بررسی کنید.</p></div><Button leftIcon={<Plus className="h-4 w-4" />}>مشتری جدید</Button></div>
      <div className="grid gap-4 md:grid-cols-4">
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-primary/10 p-3 text-primary"><UserRound className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">کل مشتریان</p><p className="text-2xl font-black text-slate-900 dark:text-white">۴,۳۲۰ نفر</p></div></CardContent></Card>
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-sky-500/10 p-3 text-sky-600"><WalletCards className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">اعضای وفادار</p><p className="text-2xl font-black text-slate-900 dark:text-white">۱,۱۸۰ نفر</p></div></CardContent></Card>
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-amber-500/10 p-3 text-amber-600"><CreditCard className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">مطالبات باز</p><p className="text-2xl font-black text-slate-900 dark:text-white">{formatCurrency(12700000)}</p></div></CardContent></Card>
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-emerald-500/10 p-3 text-emerald-600"><UserRound className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">ثبت‌نام جدید امروز</p><p className="text-2xl font-black text-slate-900 dark:text-white">۱۶ نفر</p></div></CardContent></Card>
      </div>
      <Card><CardHeader><CardTitle>فهرست مشتریان</CardTitle><CardDescription>پایش حساب مشتری، وضعیت وفاداری و آخرین تعاملات خرید</CardDescription></CardHeader><CardContent><DataTable columns={columns} data={customers} caption="اطلاعات مشتریان ثبت‌شده" emptyTitle="مشتری‌ای ثبت نشده است" emptyDescription="پس از افزودن مشتری، اطلاعات تماس و حساب او در این نما نمایش داده می‌شود." /></CardContent></Card>
    </div>
  );
}
