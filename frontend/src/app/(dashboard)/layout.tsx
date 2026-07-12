"use client";

import type { ReactNode } from "react";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { Navbar } from "@/components/layout/Navbar";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { useAuth } from "@/hooks/useAuth";
import { Sidebar } from "@/components/layout/Sidebar";

export default function DashboardLayout({
  children,
}: Readonly<{
  children: ReactNode;
}>) {
  const router = useRouter();
  const { isAuthenticated, isLoading } = useAuth();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.replace("/login");
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading || !isAuthenticated) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div role="status" aria-live="polite" className="flex items-center gap-3 rounded-3xl border border-border/70 bg-white/80 px-6 py-4 shadow-soft dark:bg-slate-950/80">
          <LoadingSpinner size="lg" />
          <span className="text-sm font-medium text-slate-600 dark:text-slate-300">در حال آماده‌سازی پنل مدیریتی...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-transparent">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <div className="lg:pr-72">
        <Navbar onMenuClick={() => setSidebarOpen(true)} />
        <main className="container py-6">
          <div className="space-y-6">{children}</div>
        </main>
      </div>
    </div>
  );
}
