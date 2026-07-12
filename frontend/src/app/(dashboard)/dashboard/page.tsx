import { AlertTriangle, CreditCard, Package, TrendingUp, Users, Wallet } from "lucide-react";

import { SalesChart } from "@/components/dashboard/SalesChart";
import { StatsCard } from "@/components/dashboard/StatsCard";
import { Badge } from "@/components/ui/Badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { formatCurrency, formatNumber } from "@/lib/utils";

const salesData = [
  { name: "شنبه", sales: 12800000, invoices: 18 },
  { name: "یکشنبه", sales: 14600000, invoices: 22 },
  { name: "دوشنبه", sales: 11800000, invoices: 16 },
  { name: "سه‌شنبه", sales: 16800000, invoices: 25 },
  { name: "چهارشنبه", sales: 18300000, invoices: 28 },
  { name: "پنجشنبه", sales: 21500000, invoices: 31 },
  { name: "جمعه", sales: 17400000, invoices: 21 },
];

const topProducts = [
  { name: "گلس آیفون 13", sold: 84, share: "23٪" },
  { name: "شارژر 25 وات سامسونگ", sold: 67, share: "18٪" },
  { name: "هندزفری بلوتوث QCY", sold: 58, share: "16٪" },
  { name: "قاب سیلیکونی شیائومی", sold: 49, share: "14٪" },
];

const activities = [
  { title: "ثبت فاکتور فروش جدید", detail: "فاکتور شماره ۱۰۳۲ برای مشتری وفادار ثبت شد.", time: "۱۰ دقیقه پیش", status: "success" as const },
  { title: "هشدار کمبود موجودی", detail: "موجودی کابل Type-C در شعبه مرکزی به زیر حداقل رسید.", time: "۲۵ دقیقه پیش", status: "warning" as const },
  { title: "ثبت خرید از تامین‌کننده", detail: "سفارش جدید برای برند Anker تایید شد.", time: "۱ ساعت پیش", status: "info" as const },
  { title: "اقساط سررسید امروز", detail: "۳ پرونده اقساطی نیازمند پیگیری مالی هستند.", time: "۲ ساعت پیش", status: "destructive" as const },
];

export default function DashboardHomePage() {
  return (
    <div className="space-y-6">
      <section className="flex flex-col gap-4 rounded-3xl border border-primary/10 bg-gradient-to-l from-primary/5 via-white to-white p-6 shadow-card dark:from-primary/10 dark:via-slate-950 dark:to-slate-950 lg:flex-row lg:items-center lg:justify-between">
        <div className="space-y-2">
          <Badge variant="info" className="w-fit">نمای کلی عملکرد امروز</Badge>
          <h1 className="text-3xl font-black text-slate-900 dark:text-white">داشبورد مدیریتی فروشگاه شاکار</h1>
          <p className="max-w-3xl text-sm leading-7 text-slate-600 dark:text-slate-300">
            آخرین وضعیت فروش، موجودی، مشتریان و تعهدات مالی را به‌صورت یکپارچه مشاهده کنید و تصمیم‌گیری شعب خود را سریع‌تر انجام دهید.
          </p>
        </div>
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
          <div className="rounded-2xl bg-white/70 px-4 py-3 text-center shadow-sm dark:bg-slate-900/60"><div className="text-xs text-slate-500">سفارش‌های امروز</div><div className="mt-2 text-xl font-black text-slate-900 dark:text-white">{formatNumber(31)}</div></div>
          <div className="rounded-2xl bg-white/70 px-4 py-3 text-center shadow-sm dark:bg-slate-900/60"><div className="text-xs text-slate-500">حاشیه سود</div><div className="mt-2 text-xl font-black text-emerald-600">18.6٪</div></div>
          <div className="rounded-2xl bg-white/70 px-4 py-3 text-center shadow-sm dark:bg-slate-900/60"><div className="text-xs text-slate-500">شعب فعال</div><div className="mt-2 text-xl font-black text-slate-900 dark:text-white">۳</div></div>
          <div className="rounded-2xl bg-white/70 px-4 py-3 text-center shadow-sm dark:bg-slate-900/60"><div className="text-xs text-slate-500">نرخ بازگشت مشتری</div><div className="mt-2 text-xl font-black text-sky-600">72٪</div></div>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatsCard title="فروش امروز" value={formatCurrency(21500000)} change={12.4} description="نسبت به روز گذشته" icon={<Wallet className="h-5 w-5" />} accentClassName="bg-emerald-500/10 text-emerald-600" />
        <StatsCard title="تعداد مشتریان" value={formatNumber(124)} change={8.1} description="مشتریان ثبت‌شده امروز" icon={<Users className="h-5 w-5" />} accentClassName="bg-sky-500/10 text-sky-600" />
        <StatsCard title="کالاهای کم‌موجودی" value={formatNumber(19)} change={-4.3} description="نیازمند تامین سریع" icon={<AlertTriangle className="h-5 w-5" />} accentClassName="bg-amber-500/10 text-amber-600" />
        <StatsCard title="اقساط در انتظار" value={formatCurrency(8400000)} change={6.7} description="سررسید تا پایان امروز" icon={<CreditCard className="h-5 w-5" />} accentClassName="bg-rose-500/10 text-rose-600" />
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.6fr_1fr]">
        <SalesChart data={salesData} />
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg"><Package className="h-5 w-5 text-primary" />پرفروش‌ترین کالاها</CardTitle>
            <CardDescription>محصولات برتر هفته جاری بر اساس تعداد فروش</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {topProducts.map((product, index) => (
              <div key={product.name} className="flex items-center justify-between rounded-2xl border border-border/70 bg-slate-50/80 px-4 py-3 dark:bg-slate-900/60">
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-primary/10 text-sm font-black text-primary">{formatNumber(index + 1)}</div>
                  <div><p className="font-semibold text-slate-900 dark:text-white">{product.name}</p><p className="text-xs text-slate-500">{formatNumber(product.sold)} عدد فروش</p></div>
                </div>
                <Badge variant="outline">سهم {product.share}</Badge>
              </div>
            ))}
          </CardContent>
        </Card>
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg"><TrendingUp className="h-5 w-5 text-primary" />فعالیت‌های اخیر</CardTitle>
            <CardDescription>رویدادهای مهم سیستم در ساعات گذشته</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {activities.map((activity) => (
              <div key={activity.title} className="flex items-start gap-4 rounded-2xl border border-border/70 p-4">
                <Badge variant={activity.status}>{activity.time}</Badge>
                <div className="space-y-1"><p className="font-semibold text-slate-900 dark:text-white">{activity.title}</p><p className="text-sm leading-7 text-slate-600 dark:text-slate-300">{activity.detail}</p></div>
              </div>
            ))}
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">وضعیت سریع عملیاتی</CardTitle>
            <CardDescription>شاخص‌های کلیدی برای تصمیم‌گیری مدیر شیفت</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {[
              { label: "ارسال‌های آماده تحویل", value: "۱۲ سفارش", tone: "text-sky-600" },
              { label: "درخواست مرجوعی", value: "۲ مورد", tone: "text-amber-600" },
              { label: "ثبت نقدی امروز", value: formatCurrency(9800000), tone: "text-emerald-600" },
              { label: "سفارش تامین باز", value: "۵ سفارش", tone: "text-primary" },
            ].map((item) => (
              <div key={item.label} className="flex items-center justify-between rounded-2xl border border-border/70 bg-slate-50/80 px-4 py-3 dark:bg-slate-900/60">
                <span className="text-sm text-slate-600 dark:text-slate-300">{item.label}</span>
                <span className={`text-sm font-bold ${item.tone}`}>{item.value}</span>
              </div>
            ))}
          </CardContent>
        </Card>
      </section>
    </div>
  );
}
