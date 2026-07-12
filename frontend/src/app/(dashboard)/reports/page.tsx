import { ArrowUpLeft, BarChart3, FileBarChart, PieChart, TrendingUp } from "lucide-react";

import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { formatCurrency } from "@/lib/utils";

const reportCards = [
  { title: "گزارش فروش شعب", description: "مقایسه عملکرد فروش شعب به تفکیک بازه زمانی، مدیر و کانال فروش.", metric: formatCurrency(93500000), icon: BarChart3, accent: "bg-primary/10 text-primary" },
  { title: "تحلیل سبد کالا", description: "بررسی ترکیب کالاهای پرفروش، حاشیه سود و کالاهای کندگردش.", metric: "۴۲ شاخص", icon: PieChart, accent: "bg-sky-500/10 text-sky-600" },
  { title: "گزارش مالی", description: "جمع‌بندی حساب‌های دریافتنی، پرداختنی و سود عملیاتی فروشگاه.", metric: formatCurrency(28600000), icon: FileBarChart, accent: "bg-emerald-500/10 text-emerald-600" },
];

export default function ReportsPage() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between"><div><Badge variant="info" className="mb-3 w-fit">مرکز تحلیل مدیریتی</Badge><h1 className="text-2xl font-black text-slate-900 dark:text-white">گزارشات مدیریتی</h1><p className="mt-2 text-sm leading-7 text-slate-600 dark:text-slate-300">داشبورد گزارشات برای تحلیل فروش، موجودی، مالی و رفتار مشتریان با تمرکز بر تصمیم‌گیری سریع.</p></div><Button leftIcon={<ArrowUpLeft className="h-4 w-4" />}>خروجی اکسل گزارشات</Button></div>
      <div className="grid gap-4 lg:grid-cols-3">{reportCards.map((report) => { const Icon = report.icon; return <Card key={report.title}><CardHeader className="space-y-4"><div className={`flex h-12 w-12 items-center justify-center rounded-2xl ${report.accent}`}><Icon className="h-6 w-6" /></div><div><CardTitle>{report.title}</CardTitle><CardDescription className="mt-2 leading-7">{report.description}</CardDescription></div></CardHeader><CardContent><div className="rounded-2xl border border-border/70 bg-slate-50/80 px-4 py-3 text-lg font-black text-slate-900 dark:bg-slate-900/60 dark:text-white">{report.metric}</div></CardContent></Card>; })}</div>
      <div className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <Card><CardHeader><CardTitle className="flex items-center gap-2"><TrendingUp className="h-5 w-5 text-primary" />بینش‌های امروز</CardTitle><CardDescription>خلاصه‌ای از مهم‌ترین الگوهای قابل توجه در فروشگاه</CardDescription></CardHeader><CardContent className="space-y-4">{["فروش لوازم جانبی اپل در شعبه مرکزی ۱۸٪ رشد داشته است.","کالاهای برند Anker بالاترین نرخ تبدیل را در فروش آنلاین ثبت کرده‌اند.","مطالبات اقساطی شعبه شرق نسبت به هفته قبل ۹٪ کاهش پیدا کرده است.","کمبود موجودی کابل Type-C می‌تواند روی فروش آخر هفته اثر بگذارد."].map((item) => <div key={item} className="rounded-2xl border border-border/70 p-4 text-sm leading-7 text-slate-600 dark:text-slate-300">{item}</div>)}</CardContent></Card>
        <Card><CardHeader><CardTitle>گزارشات آماده اجرا</CardTitle><CardDescription>دسترسی سریع به خروجی‌های پرتکرار مدیران</CardDescription></CardHeader><CardContent className="space-y-3">{["گزارش سود و زیان روزانه","موجودی بحرانی شعب","باشگاه مشتریان و خرید مجدد","فروش بر اساس فروشنده","تحلیل اقساط سررسید"].map((report) => <div key={report} className="flex items-center justify-between rounded-2xl border border-border/70 bg-slate-50/80 px-4 py-3 dark:bg-slate-900/60"><span className="text-sm text-slate-700 dark:text-slate-200">{report}</span><Badge variant="outline">آماده</Badge></div>)}</CardContent></Card>
      </div>
    </div>
  );
}
