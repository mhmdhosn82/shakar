import { CreditCard, Plus, Receipt, ShoppingCart } from "lucide-react";

import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { DataTable, type ColumnDef } from "@/components/ui/DataTable";
import { formatCurrency } from "@/lib/utils";
import type { SalesInvoice } from "@/types";

const invoices: SalesInvoice[] = [
  { id: 1, number: "SAL-1405-1032", branchId: 1, customerId: 1, date: "1405/04/21", totalAmount: 3180000, discountAmount: 150000, paidAmount: 3030000, status: "paid", paymentMethod: "کارتخوان", items: [] },
  { id: 2, number: "SAL-1405-1033", branchId: 2, customerId: 2, date: "1405/04/21", totalAmount: 5750000, discountAmount: 0, paidAmount: 2000000, status: "partial", paymentMethod: "اقساط", items: [] },
  { id: 3, number: "SAL-1405-1034", branchId: 1, customerId: 3, date: "1405/04/20", totalAmount: 1490000, discountAmount: 90000, paidAmount: 0, status: "draft", paymentMethod: "نقدی", items: [] },
];

const columns: ColumnDef<SalesInvoice>[] = [
  { key: "number", title: "شماره فاکتور" },
  { key: "date", title: "تاریخ" },
  { key: "totalAmount", title: "مبلغ کل", render: (value) => formatCurrency(Number(value)) },
  { key: "paymentMethod", title: "روش پرداخت" },
  { key: "status", title: "وضعیت", render: (value) => { const map = { paid: { label: "تسویه‌شده", variant: "success" as const }, partial: { label: "بخشی پرداخت شده", variant: "warning" as const }, draft: { label: "پیش‌نویس", variant: "outline" as const } }; const state = map[value as keyof typeof map] ?? { label: String(value), variant: "info" as const }; return <Badge variant={state.variant}>{state.label}</Badge>; } },
];

export default function SalesPage() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between"><div><h1 className="text-2xl font-black text-slate-900 dark:text-white">فاکتورهای فروش</h1><p className="mt-2 text-sm leading-7 text-slate-600 dark:text-slate-300">مدیریت فاکتورهای فروش، وضعیت تسویه، روش پرداخت و عملکرد روزانه صندوق‌ها در شعب مختلف.</p></div><Button leftIcon={<Plus className="h-4 w-4" />}>فاکتور فروش جدید</Button></div>
      <div className="grid gap-4 md:grid-cols-4">
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-primary/10 p-3 text-primary"><ShoppingCart className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">فروش امروز</p><p className="text-2xl font-black text-slate-900 dark:text-white">{formatCurrency(21500000)}</p></div></CardContent></Card>
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-sky-500/10 p-3 text-sky-600"><Receipt className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">فاکتورهای امروز</p><p className="text-2xl font-black text-slate-900 dark:text-white">۳۱ فاکتور</p></div></CardContent></Card>
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-amber-500/10 p-3 text-amber-600"><CreditCard className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">اقساط باز</p><p className="text-2xl font-black text-slate-900 dark:text-white">{formatCurrency(8400000)}</p></div></CardContent></Card>
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-emerald-500/10 p-3 text-emerald-600"><Receipt className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">میانگین هر فاکتور</p><p className="text-2xl font-black text-slate-900 dark:text-white">{formatCurrency(694000)}</p></div></CardContent></Card>
      </div>
      <Card><CardHeader><CardTitle>فهرست فاکتورهای فروش</CardTitle><CardDescription>نمای عملیات فروش با امکان پیگیری وضعیت پرداخت و اقساط</CardDescription></CardHeader><CardContent><DataTable columns={columns} data={invoices} caption="فاکتورهای فروش ثبت‌شده" emptyTitle="فاکتور فروشی وجود ندارد" emptyDescription="پس از ثبت اولین فروش، اطلاعات این بخش تکمیل خواهد شد." /></CardContent></Card>
    </div>
  );
}
