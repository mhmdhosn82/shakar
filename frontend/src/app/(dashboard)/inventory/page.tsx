"use client";

import { AlertTriangle, Boxes, PackageCheck, Warehouse } from "lucide-react";

import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { DataTable, type ColumnDef } from "@/components/ui/DataTable";

type InventoryRow = { id: number; branch: string; totalItems: number; reservedItems: number; lowStockItems: number; updatedAt: string; status: "healthy" | "warning" };
const inventoryRows: InventoryRow[] = [
  { id: 1, branch: "شعبه مرکزی", totalItems: 4280, reservedItems: 186, lowStockItems: 7, updatedAt: "امروز، 11:10", status: "healthy" },
  { id: 2, branch: "شعبه شرق", totalItems: 2760, reservedItems: 94, lowStockItems: 9, updatedAt: "امروز، 10:52", status: "warning" },
  { id: 3, branch: "شعبه کرج", totalItems: 1920, reservedItems: 48, lowStockItems: 3, updatedAt: "دیروز، 18:20", status: "healthy" },
];
const columns: ColumnDef<InventoryRow>[] = [
  { key: "branch", title: "شعبه / انبار" },
  { key: "totalItems", title: "کل موجودی" },
  { key: "reservedItems", title: "رزرو شده" },
  { key: "lowStockItems", title: "کم‌موجودی" },
  { key: "updatedAt", title: "آخرین به‌روزرسانی" },
  { key: "status", title: "سلامت موجودی", render: (value) => <Badge variant={value === "healthy" ? "success" : "warning"}>{value === "healthy" ? "پایدار" : "نیازمند بررسی"}</Badge> },
];

export default function InventoryPage() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between"><div><h1 className="text-2xl font-black text-slate-900 dark:text-white">انبار و موجودی</h1><p className="mt-2 text-sm leading-7 text-slate-600 dark:text-slate-300">کنترل سطح موجودی، رزروها، هشدار کمبود و پایداری انبار هر شعبه در یک محیط متمرکز.</p></div><Button variant="secondary" leftIcon={<Warehouse className="h-4 w-4" />}>ثبت انتقال بین انبارها</Button></div>
      <div className="grid gap-4 md:grid-cols-4">
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-primary/10 p-3 text-primary"><Boxes className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">کل اقلام</p><p className="text-2xl font-black text-slate-900 dark:text-white">۸,۹۶۰</p></div></CardContent></Card>
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-amber-500/10 p-3 text-amber-600"><AlertTriangle className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">کالاهای هشدار</p><p className="text-2xl font-black text-slate-900 dark:text-white">۱۹ قلم</p></div></CardContent></Card>
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-sky-500/10 p-3 text-sky-600"><PackageCheck className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">رزرو فروش</p><p className="text-2xl font-black text-slate-900 dark:text-white">۳۲۸ عدد</p></div></CardContent></Card>
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-emerald-500/10 p-3 text-emerald-600"><Warehouse className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">دقت انبارگردانی</p><p className="text-2xl font-black text-slate-900 dark:text-white">۹۷٫۵٪</p></div></CardContent></Card>
      </div>
      <Card><CardHeader><CardTitle>نمای شعب و انبارها</CardTitle><CardDescription>موجودی هر شعبه، رزروها و هشدارهای حیاتی در این بخش قابل پایش است.</CardDescription></CardHeader><CardContent><DataTable columns={columns} data={inventoryRows} caption="خلاصه عملیاتی موجودی شعب" emptyTitle="اطلاعاتی برای انبار وجود ندارد" emptyDescription="با تعریف انبار یا ثبت موجودی، داده‌ها در این نما ظاهر می‌شوند." /></CardContent></Card>
    </div>
  );
}
