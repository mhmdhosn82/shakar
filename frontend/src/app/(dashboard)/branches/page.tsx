import { Building2, MapPin, Plus, Store } from "lucide-react";

import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { DataTable, type ColumnDef } from "@/components/ui/DataTable";
import type { Branch } from "@/types";

const branches: Branch[] = [
  { id: 1, name: "شعبه مرکزی", code: "BR-001", city: "تهران", address: "خیابان جمهوری، مجتمع موبایل ایران", phone: "021-66778899", managerName: "علی محمدی", status: "active", createdAt: "2024-01-10T09:00:00Z" },
  { id: 2, name: "شعبه شرق", code: "BR-002", city: "تهران", address: "تهرانپارس، بین فلکه دوم و سوم", phone: "021-44556677", managerName: "مریم رضایی", status: "active", createdAt: "2024-03-14T09:00:00Z" },
  { id: 3, name: "شعبه کرج", code: "BR-003", city: "کرج", address: "گوهردشت، بلوار اصلی", phone: "026-12345678", managerName: "حسین یوسفی", status: "inactive", createdAt: "2024-02-05T09:00:00Z" },
];

const columns: ColumnDef<Branch>[] = [
  { key: "name", title: "نام شعبه", render: (_, row) => <div><p className="font-semibold text-slate-900 dark:text-white">{row.name}</p><p className="text-xs text-slate-500">کد: {row.code}</p></div> },
  { key: "city", title: "موقعیت", render: (_, row) => <div><p>{row.city}</p><p className="text-xs text-slate-500">{row.address}</p></div> },
  { key: "managerName", title: "مدیر شعبه" },
  { key: "phone", title: "تلفن" },
  { key: "status", title: "وضعیت", render: (value) => <Badge variant={value === "active" ? "success" : "warning"}>{value === "active" ? "فعال" : "غیرفعال"}</Badge> },
];

export default function BranchesPage() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between"><div><h1 className="text-2xl font-black text-slate-900 dark:text-white">مدیریت شعب</h1><p className="mt-2 text-sm leading-7 text-slate-600 dark:text-slate-300">اطلاعات شعب، مدیران و وضعیت عملیاتی هر واحد را در یک نمای سازمانی مدیریت کنید.</p></div><Button leftIcon={<Plus className="h-4 w-4" />}>ثبت شعبه جدید</Button></div>
      <div className="grid gap-4 md:grid-cols-3">
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-primary/10 p-3 text-primary"><Store className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">کل شعب</p><p className="text-2xl font-black text-slate-900 dark:text-white">۳ شعبه</p></div></CardContent></Card>
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-emerald-500/10 p-3 text-emerald-600"><Building2 className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">شعب فعال</p><p className="text-2xl font-black text-slate-900 dark:text-white">۲ شعبه</p></div></CardContent></Card>
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-sky-500/10 p-3 text-sky-600"><MapPin className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">پوشش جغرافیایی</p><p className="text-2xl font-black text-slate-900 dark:text-white">تهران و کرج</p></div></CardContent></Card>
      </div>
      <Card>
        <CardHeader><CardTitle>فهرست شعب</CardTitle><CardDescription>نمای حرفه‌ای برای کنترل مشخصات و وضعیت شعب سازمان</CardDescription></CardHeader>
        <CardContent><DataTable columns={columns} data={branches} caption="شعب ثبت‌شده در سامانه" emptyTitle="هنوز شعبه‌ای ثبت نشده است" emptyDescription="پس از تعریف اولین شعبه، اطلاعات آن در این بخش نمایش داده می‌شود." /></CardContent>
      </Card>
    </div>
  );
}
