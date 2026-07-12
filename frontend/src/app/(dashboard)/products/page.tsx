"use client";

import { Package, Plus, ScanLine, Warehouse } from "lucide-react";

import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { DataTable, type ColumnDef } from "@/components/ui/DataTable";
import { formatCurrency } from "@/lib/utils";
import type { Product } from "@/types";

const products: Product[] = [
  { id: 1, name: "شارژر 25 وات سامسونگ", sku: "PR-1001", barcode: "6261234500011", categoryId: 1, brandId: 1, purchasePrice: 540000, sellPrice: 690000, stock: 42, minimumStock: 12, status: "active", category: { id: 1, name: "شارژر", slug: "charger", description: "شارژر و آداپتور", status: "active" }, brand: { id: 1, name: "Samsung", slug: "samsung", country: "کره جنوبی", status: "active" } },
  { id: 2, name: "گلس آیفون 13", sku: "PR-1002", barcode: "6261234500012", categoryId: 2, brandId: 2, purchasePrice: 80000, sellPrice: 160000, stock: 130, minimumStock: 40, status: "active", category: { id: 2, name: "محافظ صفحه", slug: "screen-protector", description: "گلس و محافظ", status: "active" }, brand: { id: 2, name: "Generic", slug: "generic", country: "چین", status: "active" } },
  { id: 3, name: "هندزفری بلوتوث QCY", sku: "PR-1003", barcode: "6261234500013", categoryId: 3, brandId: 3, purchasePrice: 980000, sellPrice: 1290000, stock: 9, minimumStock: 15, status: "active", category: { id: 3, name: "هندزفری", slug: "headset", description: "انواع هندزفری", status: "active" }, brand: { id: 3, name: "QCY", slug: "qcy", country: "چین", status: "active" } },
];

const columns: ColumnDef<Product>[] = [
  { key: "name", title: "کالا", render: (_, row) => <div><p className="font-semibold text-slate-900 dark:text-white">{row.name}</p><p className="text-xs text-slate-500">SKU: {row.sku}</p></div> },
  { key: "category", title: "دسته‌بندی", render: (_, row) => row.category?.name ?? "-" },
  { key: "brand", title: "برند", render: (_, row) => row.brand?.name ?? "-" },
  { key: "sellPrice", title: "قیمت فروش", render: (value) => formatCurrency(Number(value)) },
  { key: "stock", title: "موجودی", render: (_, row) => <div className="flex items-center gap-2"><span>{row.stock} عدد</span>{row.stock <= row.minimumStock ? <Badge variant="warning">کم‌موجود</Badge> : <Badge variant="success">مناسب</Badge>}</div> },
];

export default function ProductsPage() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between"><div><h1 className="text-2xl font-black text-slate-900 dark:text-white">کاتالوگ کالاها</h1><p className="mt-2 text-sm leading-7 text-slate-600 dark:text-slate-300">مدیریت حرفه‌ای کالاها، قیمت‌ها، موجودی و سطح حداقل انبار برای فروشگاه و شعب مختلف.</p></div><div className="flex gap-3"><Button variant="secondary" leftIcon={<ScanLine className="h-4 w-4" />}>اسکن بارکد</Button><Button leftIcon={<Plus className="h-4 w-4" />}>کالای جدید</Button></div></div>
      <div className="grid gap-4 md:grid-cols-3">
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-primary/10 p-3 text-primary"><Package className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">کالاهای فعال</p><p className="text-2xl font-black text-slate-900 dark:text-white">۱,۲۸۰ قلم</p></div></CardContent></Card>
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-amber-500/10 p-3 text-amber-600"><Warehouse className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">کمبود موجودی</p><p className="text-2xl font-black text-slate-900 dark:text-white">۱۹ کالا</p></div></CardContent></Card>
        <Card><CardContent className="flex items-center gap-4 p-6"><div className="rounded-2xl bg-emerald-500/10 p-3 text-emerald-600"><ScanLine className="h-6 w-6" /></div><div><p className="text-sm text-slate-500">پوشش بارکد</p><p className="text-2xl font-black text-slate-900 dark:text-white">۹۸٪</p></div></CardContent></Card>
      </div>
      <Card><CardHeader><CardTitle>فهرست کالاها</CardTitle><CardDescription>نمایش دقیق مشخصات، برند، قیمت و وضعیت موجودی هر محصول</CardDescription></CardHeader><CardContent><DataTable columns={columns} data={products} caption="لیست کالاهای قابل فروش" emptyTitle="کالایی موجود نیست" emptyDescription="پس از ثبت اولین کالا، اطلاعات آن در این بخش قرار می‌گیرد." /></CardContent></Card>
    </div>
  );
}
