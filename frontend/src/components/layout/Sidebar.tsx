"use client";

import {
  BarChart3,
  Boxes,
  Building2,
  ChevronDown,
  DatabaseBackup,
  Files,
  LayoutDashboard,
  Layers3,
  Package,
  ShoppingCart,
  Truck,
  UserCog,
  Users,
  WalletCards,
  X,
} from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import type { ComponentType } from "react";
import { useMemo, useState } from "react";

import { cn } from "@/lib/utils";

type SidebarProps = {
  isOpen?: boolean;
  onClose?: () => void;
};

type NavItem = {
  title: string;
  href: string;
  icon: ComponentType<{ className?: string }>;
};

type NavSection = {
  title: string;
  items: NavItem[];
};

const sections: NavSection[] = [
  { title: "داشبورد", items: [{ title: "نمای اصلی", href: "/dashboard", icon: LayoutDashboard }] },
  {
    title: "مدیریت",
    items: [
      { title: "کاربران", href: "/users", icon: UserCog },
      { title: "شعبات", href: "/branches", icon: Building2 },
    ],
  },
  {
    title: "انبار و کالا",
    items: [
      { title: "کالاها", href: "/products", icon: Package },
      { title: "دسته‌بندی", href: "/categories", icon: Layers3 },
      { title: "برند", href: "/brands", icon: WalletCards },
      { title: "انبار", href: "/inventory", icon: Boxes },
    ],
  },
  {
    title: "خرید و فروش",
    items: [
      { title: "فروش", href: "/sales", icon: ShoppingCart },
      { title: "خرید", href: "/purchases", icon: Truck },
      { title: "مشتریان", href: "/customers", icon: Users },
      { title: "تامین‌کنندگان", href: "/suppliers", icon: Truck },
    ],
  },
  {
    title: "حسابداری",
    items: [
      { title: "حساب‌ها", href: "/accounting", icon: WalletCards },
      { title: "اسناد مالی", href: "/accounting#documents", icon: Files },
    ],
  },
  { title: "گزارشات", items: [{ title: "مرکز گزارشات", href: "/reports", icon: BarChart3 }] },
  { title: "تنظیمات", items: [{ title: "پشتیبان‌گیری", href: "/backup", icon: DatabaseBackup }] },
];

export function Sidebar({ isOpen = false, onClose }: SidebarProps) {
  const pathname = usePathname();
  const [collapsedSections, setCollapsedSections] = useState<Record<string, boolean>>({});
  const normalizedPath = useMemo(() => pathname.replace(/\/$/, "") || "/", [pathname]);

  const toggleSection = (title: string) => {
    setCollapsedSections((current) => ({ ...current, [title]: !current[title] }));
  };

  return (
    <>
      <div className={cn("fixed inset-0 z-40 bg-slate-950/45 backdrop-blur-sm transition-opacity duration-300 lg:hidden", isOpen ? "pointer-events-auto opacity-100" : "pointer-events-none opacity-0")} onClick={onClose} />
      <aside className={cn("fixed inset-y-0 right-0 z-50 flex w-72 flex-col border-l border-white/60 bg-slate-950 px-4 py-4 text-slate-100 shadow-2xl transition-transform duration-300 lg:translate-x-0", isOpen ? "translate-x-0" : "translate-x-full lg:translate-x-0")}>
        <div className="mb-4 flex items-center justify-between rounded-3xl border border-white/10 bg-white/5 p-4">
          <Link href="/dashboard" className="flex items-center gap-3" onClick={onClose}>
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-primary to-sky-500 text-2xl font-black text-white shadow-lg shadow-primary/30">ش</div>
            <div>
              <p className="text-lg font-black">شاکار</p>
              <p className="text-xs text-slate-400">Retail Management Platform</p>
            </div>
          </Link>
          <button type="button" className="rounded-2xl p-2 text-slate-300 transition hover:bg-white/10 hover:text-white lg:hidden" onClick={onClose} aria-label="بستن منو">
            <X className="h-5 w-5" />
          </button>
        </div>

        <div className="mb-4 rounded-3xl border border-primary/15 bg-primary/10 p-4 text-sm leading-7 text-slate-200">
          نمای یکپارچه مدیریت فروش، موجودی، حسابداری و گزارشات برای فروشگاه‌های موبایل و لوازم جانبی.
        </div>

        <nav className="flex-1 space-y-3 overflow-y-auto pb-6">
          {sections.map((section) => {
            const isCollapsed = collapsedSections[section.title] ?? false;
            return (
              <div key={section.title} className="rounded-3xl border border-white/8 bg-white/5 p-2">
                <button type="button" onClick={() => toggleSection(section.title)} className="flex w-full items-center justify-between rounded-2xl px-3 py-3 text-xs font-bold text-slate-300 transition hover:bg-white/6 hover:text-white">
                  <span>{section.title}</span>
                  <ChevronDown className={cn("h-4 w-4 transition-transform", isCollapsed && "rotate-180")} />
                </button>
                {!isCollapsed ? (
                  <div className="mt-1 space-y-1">
                    {section.items.map((item) => {
                      const targetPath = item.href.split("#")[0];
                      const isActive = targetPath === "/dashboard" ? normalizedPath === "/dashboard" : normalizedPath === targetPath || normalizedPath.startsWith(`${targetPath}/`);
                      const Icon = item.icon;
                      return (
                        <Link key={item.href} href={item.href} onClick={onClose} className={cn("group relative flex items-center gap-3 rounded-2xl px-3 py-3 text-sm text-slate-300 transition-all duration-200 hover:bg-white/10 hover:text-white", isActive && "bg-gradient-to-l from-primary/25 to-sky-500/10 text-white shadow-lg shadow-primary/10")}>
                          <span className={cn("absolute bottom-2 right-1 top-2 w-1 rounded-full bg-transparent transition-all", isActive && "bg-primary shadow-[0_0_12px_rgba(99,102,241,0.8)]")} />
                          <span className={cn("flex h-9 w-9 items-center justify-center rounded-2xl bg-white/5 text-slate-300 transition group-hover:bg-white/10 group-hover:text-white", isActive && "bg-white/10 text-white")}>
                            <Icon className="h-4 w-4" />
                          </span>
                          <span className="font-medium">{item.title}</span>
                        </Link>
                      );
                    })}
                  </div>
                ) : null}
              </div>
            );
          })}
        </nav>
      </aside>
    </>
  );
}
