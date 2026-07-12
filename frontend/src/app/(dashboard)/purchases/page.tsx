import { ClipboardList, PackagePlus, Plus, Truck } from "lucide-react";

import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { DataTable, type ColumnDef } from "@/components/ui/DataTable";
import { formatCurrency } from "@/lib/utils";
import type { PurchaseInvoice } from "@/types";

const purchaseInvoices: PurchaseInvoice[] = [
  { id: 1, number: "PUR-1405-210", supplierId: 1, branchId: 1, date: "1405/04/19", totalAmount: 18400000, paidAmount: 10000000, dueDate: "1405/04/28", status: "partial" },
  { id: 2, number: "PUR-1405-211", supplierId: 2, branchId: 2, date: "1405/04/20", totalAmount: 9600000, paidAmount: 9600000, dueDate: "1405/04/20", status: "paid" },
  { id: 3, number: "PUR-1405-212", supplierId: 3, branchId: 1, date: "1405/04/21", totalAmount: 12300000, paidAmount: 0, dueDate: "1405/04/30", status: "pending" },
];

const columns: ColumnDef<PurchaseInvoice>[] = [
  { key: "number", title: "شماره سند" },
  { key: "date", title: "تاریخ خرید" },
  { key: "totalAmount", title: "جمع فاکتور", render: (value) => formatCurrency(Number(value)) },
  { key: "dueDate", title: "سررسید" },
  { key: "status", title: "وضعیت", render: (value) => { const variants = { paid: { label: "تسویه‌شده", variant: "success" as const }, partial: { label: "بخشی پرداخت شده", variant: "warning" as const }, pending: { label: "در انتظار", variant: "info" as const } }; const item = variants[value as keyof typeof variants] ?? { label: String(value), variant: "outline" as const }; return <Badge variant={item.variant}>{item.label}</Badge>; } },
];

export default function PurchasesPage() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between"><div><h1 className="text-2xl font-black text-slate-900 dark:text-white">فاکتورهای خرید</h1><p className="mt-2 text-sm leading-7 text-slate-600 dark:text-slate-300">خریدهای تامین‌کنندگان، مبالغ قابل پرداخت و برنامه ورود کالا به انبار را مدیریت کنید.</p></div><Button leftIcon={<Plus className="h-4 w-4" />}>ثبت خرید جدید</Button></div>
      <div className="grid gap-4 md:grid-cols-4">
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-primary/10 p-3 text-primary"><PackagePlus className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">خرید این هفته</p><p className="text-2xl font-black text-slate-900 dark:text-white">{formatCurrency(40200000)}</p></div></CardContent></Card>
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-sky-500/10 p-3 text-sky-600"><Truck className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">محموله‌های در راه</p><p className="text-2xl font-black text-slate-900 dark:text-white">۵ محموله</p></div></CardContent></Card>
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-amber-500/10 p-3 text-amber-600"><ClipboardList className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">تعهدات پرداخت</p><p className="text-2xl font-black text-slate-900 dark:text-white">{formatCurrency(20700000)}</p></div></CardContent></Card>
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-emerald-500/10 p-3 text-emerald-600"><PackagePlus className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">درصد تسویه</p><p className="text-2xl font-black text-slate-900 dark:text-white">۶۲٪</p></div></CardContent></Card>
      </div>
      <Card><CardHeader><CardTitle>فهرست فاکتورهای خرید</CardTitle><CardDescription>کنترل هزینه تامین و وضعیت تسویه اسناد خرید در یک نمای کامل</CardDescription></CardHeader><CardContent><DataTable columns={columns} data={purchaseInvoices} caption="اسناد خرید ثبت‌شده" emptyTitle="فاکتور خریدی وجود ندارد" emptyDescription="با ثبت اولین خرید، اطلاعات سند در این جدول ظاهر می‌شود." /></CardContent></Card>
    </div>
  );
}
