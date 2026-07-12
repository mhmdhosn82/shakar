import type { Metadata } from "next";
import type { ReactNode } from "react";

import { Providers } from "@/components/providers/Providers";

import "./globals.css";

export const metadata: Metadata = {
  title: "فروشگاه شاکار",
  description:
    "پلتفرم حرفه‌ای مدیریت فروشگاه موبایل و لوازم جانبی با ماژول‌های فروش، انبار، حسابداری و گزارشات مدیریتی.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: ReactNode;
}>) {
  return (
    <html lang="fa" dir="rtl" suppressHydrationWarning>
      <body className="min-h-screen bg-background font-sans text-foreground antialiased">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
