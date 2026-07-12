"use client";

import { Clock3, Handshake, Plus, Truck } from "lucide-react";

import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { DataTable, type ColumnDef } from "@/components/ui/DataTable";
import type { Supplier } from "@/types";

const suppliers: Supplier[] = [
  { id: 1, name: "پارس همراه", contactName: "خانم عباسی", phone: "021-77889911", email: "sales@parshamrah.ir", status: "active", leadTimeDays: 2, balance: 4300000, lastPurchaseAt: "1405/04/18", createdAt: "2024-01-11T09:00:00Z" },
  { id: 2, name: "همراه پخش آرین", contactName: "آقای سلیمی", phone: "021-88997744", email: "order@arian-distribution.ir", status: "active", leadTimeDays: 4, balance: 0, lastPurchaseAt: "1405/04/20", createdAt: "2024-02-02T09:00:00Z" },
  { id: 3, name: "تجارت اکسسوری شرق", contactName: "خانم میرزایی", phone: "026-33445566", email: "supply@sharq-accessory.ir", status: "inactive", leadTimeDays: 7, balance: 1280000, lastPurchaseAt: "1405/04/05", createdAt: "2024-03-04T09:00:00Z" },
];

const columns: ColumnDef<Supplier>[] = [
  { key: "name", title: "تامین‌کننده", render: (_, row) => <div><p className="font-semibold text-slate-900 dark:text-white">{row.name}</p><p className="text-xs text-slate-500">{row.contactName}</p></div> },
  { key: "phone", title: "شماره تماس" },
  { key: "leadTimeDays", title: "زمان تامین", render: (value) => `${value} روز` },
  { key: "lastPurchaseAt", title: "آخرین خرید" },
  { key: "status", title: "وضعیت", render: (value) => <Badge variant={value === "active" ? "success" : "outline"}>{value === "active" ? "همکار فعال" : "متوقف"}</Badge> },
];

export default function SuppliersPage() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between"><div><h1 className="text-2xl font-black text-slate-900 dark:text-white">تامین‌کنندگان</h1><p className="mt-2 text-sm leading-7 text-slate-600 dark:text-slate-300">فهرست تامین‌کنندگان، مدت زمان تحویل، همکاری فعال و وضعیت تسویه هر شریک تجاری را رصد کنید.</p></div><Button leftIcon={<Plus className="h-4 w-4" />}>تامین‌کننده جدید</Button></div>
      <div className="grid gap-4 md:grid-cols-4">
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-primary/10 p-3 text-primary"><Handshake className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">تامین‌کنندگان فعال</p><p className="text-2xl font-black text-slate-900 dark:text-white">۲۴ شرکت</p></div></CardContent></Card>
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-sky-500/10 p-3 text-sky-600"><Truck className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">ارسال‌های در راه</p><p className="text-2xl font-black text-slate-900 dark:text-white">۷ محموله</p></div></CardContent></Card>
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-amber-500/10 p-3 text-amber-600"><Clock3 className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">میانگین زمان تحویل</p><p className="text-2xl font-black text-slate-900 dark:text-white">۳٫۸ روز</p></div></CardContent></Card>
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-emerald-500/10 p-3 text-emerald-600"><Handshake className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">تسویه به‌موقع</p><p className="text-2xl font-black text-slate-900 dark:text-white">۹۱٪</p></div></CardContent></Card>
      </div>
      <Card><CardHeader><CardTitle>فهرست تامین‌کنندگان</CardTitle><CardDescription>اطلاعات ارتباطی، زمان تامین و کیفیت همکاری در یک جدول عملیاتی</CardDescription></CardHeader><CardContent><DataTable columns={columns} data={suppliers} caption="تامین‌کنندگان ثبت‌شده در سامانه" emptyTitle="تامین‌کننده‌ای تعریف نشده است" emptyDescription="پس از ثبت تامین‌کننده جدید، اطلاعات تماس و همکاری او اینجا نمایش داده می‌شود." /></CardContent></Card>
    </div>
  );
}
