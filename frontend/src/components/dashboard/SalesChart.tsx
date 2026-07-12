"use client";

import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { formatCurrency } from "@/lib/utils";

type SalesChartPoint = { name: string; sales: number; invoices?: number };

export function SalesChart({ data }: { data: SalesChartPoint[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">روند فروش هفتگی</CardTitle>
        <CardDescription>نمایش فروش روزانه و حجم تراکنش‌ها در یک نگاه</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-[320px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data} margin={{ top: 12, right: 18, left: 18, bottom: 0 }}>
              <defs>
                <linearGradient id="sales-gradient" x1="0" x2="0" y1="0" y2="1">
                  <stop offset="5%" stopColor="#4F46E5" stopOpacity={0.28} />
                  <stop offset="95%" stopColor="#4F46E5" stopOpacity={0.02} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="4 4" vertical={false} stroke="rgba(148, 163, 184, 0.24)" />
              <XAxis dataKey="name" tickLine={false} axisLine={false} tick={{ fill: "#64748B", fontSize: 12 }} />
              <YAxis tickFormatter={(value) => `${Math.round(Number(value) / 1000000)}م`} tickLine={false} axisLine={false} tick={{ fill: "#64748B", fontSize: 12 }} />
              <Tooltip formatter={(value: number) => [formatCurrency(value), "فروش"]} contentStyle={{ borderRadius: "16px", border: "1px solid rgba(226, 232, 240, 0.9)", background: "rgba(255,255,255,0.95)", boxShadow: "0 20px 40px -24px rgba(15, 23, 42, 0.35)", direction: "rtl" }} labelStyle={{ color: "#0F172A", fontWeight: 700 }} />
              <Area type="monotone" dataKey="sales" stroke="#4F46E5" strokeWidth={3} fill="url(#sales-gradient)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}
