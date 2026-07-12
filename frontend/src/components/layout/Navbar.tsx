"use client";

import { Bell, ChevronDown, LogOut, Menu, Store, UserCircle2 } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useMemo, useState } from "react";

import { Button } from "@/components/ui/Button";
import { useAuth } from "@/hooks/useAuth";
import { formatDate } from "@/lib/utils";

const pageTitles: Record<string, { title: string; subtitle: string }> = {
  "/dashboard": { title: "داشبورد مدیریتی", subtitle: "نمای کلی عملیات فروشگاه و شعب" },
  "/branches": { title: "شعب", subtitle: "مدیریت ساختار سازمانی و شعب فروشگاه" },
  "/users": { title: "کاربران", subtitle: "کنترل دسترسی‌ها و نقش‌های سازمانی" },
  "/products": { title: "کالاها", subtitle: "کاتالوگ حرفه‌ای محصولات و قیمت‌ها" },
  "/categories": { title: "دسته‌بندی‌ها", subtitle: "ساختار محصول و طبقه‌بندی کالاها" },
  "/brands": { title: "برندها", subtitle: "مدیریت برندهای فعال و تامین‌کنندگان" },
  "/inventory": { title: "انبار", subtitle: "پایش موجودی و گردش کالا" },
  "/customers": { title: "مشتریان", subtitle: "تحلیل مشتریان و مانده حساب" },
  "/suppliers": { title: "تامین‌کنندگان", subtitle: "کنترل همکاری و زمان‌بندی تامین" },
  "/sales": { title: "فروش", subtitle: "فاکتورهای فروش و اقساط" },
  "/purchases": { title: "خرید", subtitle: "مدیریت سفارش‌ها و اسناد خرید" },
  "/accounting": { title: "حسابداری", subtitle: "چارت حساب‌ها و اسناد مالی" },
  "/reports": { title: "گزارشات", subtitle: "مرکز تحلیل مدیریتی و گزارشات سازمانی" },
  "/backup": { title: "پشتیبان‌گیری", subtitle: "امنیت، نسخه‌برداری و بازیابی اطلاعات" },
};

const branches = ["شعبه مرکزی", "شعبه شرق", "شعبه کرج"];

export function Navbar({ onMenuClick }: { onMenuClick?: () => void }) {
  const pathname = usePathname();
  const { user, logout } = useAuth();
  const [now, setNow] = useState(new Date());
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    const timer = window.setInterval(() => setNow(new Date()), 60000);
    return () => window.clearInterval(timer);
  }, []);

  const meta = useMemo(() => pageTitles[pathname] ?? pageTitles["/dashboard"], [pathname]);

  return (
    <header className="sticky top-0 z-30 border-b border-white/60 bg-white/80 backdrop-blur-xl dark:border-slate-800/80 dark:bg-slate-950/80">
      <div className="container flex flex-col gap-4 py-4 lg:flex-row lg:items-center lg:justify-between">
        <div className="flex items-center gap-3">
          <Button variant="ghost" size="icon" className="lg:hidden" onClick={onMenuClick} aria-label="باز کردن منو">
            <Menu className="h-5 w-5" />
          </Button>
          <Link href="/dashboard" className="flex items-center gap-3 lg:hidden">
            <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-primary text-white">
              <Store className="h-5 w-5" />
            </div>
          </Link>
          <div>
            <h2 className="text-xl font-black text-slate-900 dark:text-white">{meta.title}</h2>
            <p className="text-sm text-slate-500 dark:text-slate-400">{meta.subtitle}</p>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <div className="hidden rounded-2xl border border-border/70 bg-slate-50/80 px-4 py-2 text-sm text-slate-600 dark:bg-slate-900/70 dark:text-slate-300 md:block">
            {formatDate(now, { dateStyle: "full", timeStyle: "short" })}
          </div>

          <label className="flex items-center gap-3 rounded-2xl border border-border/70 bg-white/80 px-4 py-2 text-sm shadow-sm dark:bg-slate-900/70">
            <span className="text-slate-500 dark:text-slate-400">شعبه فعال</span>
            <select className="bg-transparent font-medium text-slate-900 outline-none dark:text-white">
              {branches.map((branch) => (
                <option key={branch}>{branch}</option>
              ))}
            </select>
          </label>

          <button type="button" className="relative rounded-2xl border border-border/70 bg-white/80 p-3 text-slate-600 shadow-sm transition hover:text-primary dark:bg-slate-900/70 dark:text-slate-300" aria-label="اعلان‌ها">
            <Bell className="h-5 w-5" />
            <span className="absolute right-2 top-2 flex h-2.5 w-2.5 rounded-full bg-rose-500" />
          </button>

          <div className="relative">
            <button type="button" className="flex items-center gap-3 rounded-2xl border border-border/70 bg-white/80 px-4 py-2 shadow-sm transition hover:border-primary/30 dark:bg-slate-900/70" onClick={() => setMenuOpen((value) => !value)}>
              <div className="text-right">
                <p className="text-sm font-semibold text-slate-900 dark:text-white">{user?.fullName ?? "کاربر سیستم"}</p>
                <p className="text-xs text-slate-500 dark:text-slate-400">{user?.role?.name ?? "مدیر شعبه"}</p>
              </div>
              <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-primary/10 text-primary">
                <UserCircle2 className="h-5 w-5" />
              </div>
              <ChevronDown className="h-4 w-4 text-slate-400" />
            </button>

            {menuOpen ? (
              <div className="absolute left-0 top-[calc(100%+0.75rem)] z-20 w-56 rounded-3xl border border-border/70 bg-white p-2 shadow-card dark:bg-slate-950">
                <button type="button" className="flex w-full items-center gap-3 rounded-2xl px-3 py-3 text-sm text-slate-700 transition hover:bg-slate-50 dark:text-slate-200 dark:hover:bg-slate-900">
                  <UserCircle2 className="h-4 w-4" />
                  پروفایل کاربر
                </button>
                <button type="button" className="flex w-full items-center gap-3 rounded-2xl px-3 py-3 text-sm text-rose-600 transition hover:bg-rose-50 dark:hover:bg-rose-950/30" onClick={() => { setMenuOpen(false); logout(); }}>
                  <LogOut className="h-4 w-4" />
                  خروج از حساب
                </button>
              </div>
            ) : null}
          </div>
        </div>
      </div>
    </header>
  );
}
