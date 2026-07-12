import * as React from "react";

import { cn } from "@/lib/utils";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  hint?: string;
  leftIcon?: React.ReactNode;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type = "text", label, error, hint, leftIcon, ...props }, ref) => {
    return (
      <label className="block space-y-2">
        {label ? <span className="text-sm font-semibold text-slate-700 dark:text-slate-200">{label}</span> : null}
        <span
          className={cn(
            "flex items-center gap-3 rounded-2xl border bg-white px-4 py-3 shadow-sm transition focus-within:border-primary focus-within:ring-2 focus-within:ring-primary/20 dark:bg-slate-950",
            error ? "border-red-300 focus-within:border-red-500 focus-within:ring-red-500/20" : "border-border/70",
          )}
        >
          {leftIcon ? <span className="text-slate-400">{leftIcon}</span> : null}
          <input
            ref={ref}
            type={type}
            className={cn(
              "h-6 w-full border-0 bg-transparent text-sm text-slate-900 outline-none placeholder:text-slate-400 dark:text-white",
              className,
            )}
            {...props}
          />
        </span>
        {error ? (
          <span className="text-sm text-red-600 dark:text-red-400">{error}</span>
        ) : hint ? (
          <span className="text-sm text-slate-500 dark:text-slate-400">{hint}</span>
        ) : null}
      </label>
    );
  },
);

Input.displayName = "Input";
