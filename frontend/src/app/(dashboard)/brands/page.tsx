import { BadgeCheck, Globe2, Plus, Tags } from "lucide-react";

import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { DataTable, type ColumnDef } from "@/components/ui/DataTable";
import type { Brand } from "@/types";

const brands: Brand[] = [
  { id: 1, name: "Samsung", slug: "samsung", country: "کره جنوبی", status: "active", productsCount: 112 },
  { id: 2, name: "Anker", slug: "anker", country: "چین", status: "active", productsCount: 46 },
  { id: 3, name: "QCY", slug: "qcy", country: "چین", status: "active", productsCount: 37 },
  { id: 4, name: "Remax", slug: "remax", country: "چین", status: "inactive", productsCount: 22 },
];

const columns: ColumnDef<Brand>[] = [
  { key: "name", title: "برند" },
  { key: "country", title: "کشور مبدا" },
  { key: "productsCount", title: "تعداد کالا" },
  { key: "status", title: "وضعیت", render: (value) => <Badge variant={value === "active" ? "success" : "warning"}>{value === "active" ? "فعال" : "غیرفعال"}</Badge> },
];

export default function BrandsPage() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between"><div><h1 className="text-2xl font-black text-slate-900 dark:text-white">مدیریت برندها</h1><p className="mt-2 text-sm leading-7 text-slate-600 dark:text-slate-300">برندهای تامین‌کنندگان و کالاها را برای یکپارچگی کاتالوگ و گزارشات برندمحور کنترل کنید.</p></div><Button leftIcon={<Plus className="h-4 w-4" />}>برند جدید</Button></div>
      <div className="grid gap-4 md:grid-cols-3">
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-primary/10 p-3 text-primary"><Tags className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">برندهای ثبت‌شده</p><p className="text-2xl font-black text-slate-900 dark:text-white">۴ برند</p></div></CardContent></Card>
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-sky-500/10 p-3 text-sky-600"><Globe2 className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">مبدا تامین</p><p className="text-2xl font-black text-slate-900 dark:text-white">۳ کشور</p></div></CardContent></Card>
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-emerald-500/10 p-3 text-emerald-600"><BadgeCheck className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">برندهای فعال</p><p className="text-2xl font-black text-slate-900 dark:text-white">۳ برند</p></div></CardContent></Card>
      </div>
      <Card><CardHeader><CardTitle>فهرست برندها</CardTitle><CardDescription>مدیریت برندها برای تحلیل فروش، موجودی و تامین‌کنندگان</CardDescription></CardHeader><CardContent><DataTable columns={columns} data={brands} caption="برندهای تعریف‌شده" emptyTitle="برندی ثبت نشده است" emptyDescription="پس از ایجاد اولین برند، اطلاعات آن در این جدول قرار خواهد گرفت." /></CardContent></Card>
    </div>
  );
}
