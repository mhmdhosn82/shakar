import * as React from "react";

import { cn } from "@/lib/utils";

const variants = {
  default: "bg-primary/10 text-primary",
  success: "bg-emerald-500/12 text-emerald-700 dark:text-emerald-300",
  warning: "bg-amber-500/12 text-amber-700 dark:text-amber-300",
  destructive: "bg-rose-500/12 text-rose-700 dark:text-rose-300",
  info: "bg-sky-500/12 text-sky-700 dark:text-sky-300",
  outline: "border border-border/80 bg-transparent text-slate-600 dark:text-slate-300",
} as const;

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: keyof typeof variants;
}

export function Badge({ className, variant = "default", ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-3 py-1 text-xs font-bold",
        variants[variant],
        className,
      )}
      {...props}
    />
  );
}
