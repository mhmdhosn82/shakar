import { FileSpreadsheet, Landmark, Plus, Scale } from "lucide-react";

import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { DataTable, type ColumnDef } from "@/components/ui/DataTable";
import { formatCurrency } from "@/lib/utils";
import type { Account } from "@/types";

const accounts: Account[] = [
  { id: 1, code: "1101", name: "صندوق شعبه مرکزی", type: "asset", balance: 12850000, status: "active" },
  { id: 2, code: "1201", name: "بانک ملت", type: "asset", balance: 46800000, status: "active" },
  { id: 3, code: "2101", name: "حساب‌های پرداختنی", type: "liability", balance: 20700000, status: "active" },
  { id: 4, code: "4101", name: "درآمد فروش کالا", type: "income", balance: 93500000, status: "active" },
];

const columns: ColumnDef<Account>[] = [
  { key: "code", title: "کد حساب", render: (_, row) => <div><p className="font-semibold text-slate-900 dark:text-white">{row.code}</p><p className="text-xs text-slate-500">{row.name}</p></div> },
  { key: "type", title: "ماهیت", render: (value) => ({ asset: "دارایی", liability: "بدهی", equity: "سرمایه", income: "درآمد", expense: "هزینه" }[value as string] ?? String(value)) },
  { key: "balance", title: "مانده", render: (value) => formatCurrency(Number(value)) },
  { key: "status", title: "وضعیت", render: () => <Badge variant="success">فعال</Badge> },
];

export default function AccountingPage() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between"><div><h1 className="text-2xl font-black text-slate-900 dark:text-white">حسابداری و سرفصل‌ها</h1><p className="mt-2 text-sm leading-7 text-slate-600 dark:text-slate-300">سرفصل‌های حسابداری، مانده حساب‌ها و خلاصه اسناد مالی را برای کنترل دقیق مالی مشاهده کنید.</p></div><div className="flex gap-3"><Button variant="secondary" leftIcon={<FileSpreadsheet className="h-4 w-4" />}>اسناد مالی</Button><Button leftIcon={<Plus className="h-4 w-4" />}>حساب جدید</Button></div></div>
      <div className="grid gap-4 md:grid-cols-4">
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-primary/10 p-3 text-primary"><Landmark className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">نقد و بانک</p><p className="text-2xl font-black text-slate-900 dark:text-white">{formatCurrency(59650000)}</p></div></CardContent></Card>
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-sky-500/10 p-3 text-sky-600"><Scale className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">بدهی جاری</p><p className="text-2xl font-black text-slate-900 dark:text-white">{formatCurrency(20700000)}</p></div></CardContent></Card>
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-emerald-500/10 p-3 text-emerald-600"><FileSpreadsheet className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">سند ثبت امروز</p><p className="text-2xl font-black text-slate-900 dark:text-white">۱۸ سند</p></div></CardContent></Card>
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-amber-500/10 p-3 text-amber-600"><Scale className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">سود ناخالص ماه</p><p className="text-2xl font-black text-slate-900 dark:text-white">{formatCurrency(28600000)}</p></div></CardContent></Card>
      </div>
      <Card><CardHeader><CardTitle>چارت حساب‌ها</CardTitle><CardDescription>سرفصل‌های کلیدی حسابداری برای کنترل جریان مالی فروشگاه</CardDescription></CardHeader><CardContent><DataTable columns={columns} data={accounts} caption="چارت حساب‌های اصلی" emptyTitle="حسابی تعریف نشده است" emptyDescription="پس از ایجاد سرفصل‌های مالی، اطلاعات آن‌ها در این جدول قرار می‌گیرد." /></CardContent></Card>
    </div>
  );
}
