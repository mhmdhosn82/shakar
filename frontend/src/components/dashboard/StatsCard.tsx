import { ArrowDownLeft, ArrowUpRight } from "lucide-react";

import { Card, CardContent } from "@/components/ui/Card";
import { cn } from "@/lib/utils";

interface StatsCardProps {
  title: string;
  value: string;
  change: number;
  description?: string;
  icon: React.ReactNode;
  accentClassName?: string;
}

export function StatsCard({ title, value, change, description, icon, accentClassName }: StatsCardProps) {
  const positive = change >= 0;
  return (
    <Card>
      <CardContent className="p-6">
        <div className="flex items-start justify-between gap-4">
          <div className="space-y-3">
            <p className="text-sm font-medium text-slate-500 dark:text-slate-400">{title}</p>
            <p className="text-3xl font-black text-slate-900 dark:text-white">{value}</p>
            <div className="flex flex-wrap items-center gap-2 text-sm">
              <span className={cn("inline-flex items-center gap-1 rounded-full px-2.5 py-1 font-bold", positive ? "bg-emerald-500/12 text-emerald-700 dark:text-emerald-300" : "bg-rose-500/12 text-rose-700 dark:text-rose-300")}>{positive ? <ArrowUpRight className="h-3.5 w-3.5" /> : <ArrowDownLeft className="h-3.5 w-3.5" />}{Math.abs(change)}٪</span>
              {description ? <span className="text-slate-500 dark:text-slate-400">{description}</span> : null}
            </div>
          </div>
          <div className={cn("flex h-14 w-14 items-center justify-center rounded-3xl", accentClassName ?? "bg-primary/10 text-primary")}>{icon}</div>
        </div>
      </CardContent>
    </Card>
  );
}
