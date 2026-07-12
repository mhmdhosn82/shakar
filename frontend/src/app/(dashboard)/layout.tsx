"use client";

import { useState } from "react";

import { Navbar } from "@/components/layout/Navbar";
import { Sidebar } from "@/components/layout/Sidebar";

export default function DashboardLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

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
