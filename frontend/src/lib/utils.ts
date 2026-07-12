import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatNumber(value: number) {
  if (!Number.isFinite(value)) return new Intl.NumberFormat("fa-IR").format(0);
  return new Intl.NumberFormat("fa-IR").format(value);
}

export function formatCurrency(value: number, currencyLabel = "تومان") {
  if (!Number.isFinite(value)) return `۰ ${currencyLabel}`;
  return `${formatNumber(value)} ${currencyLabel}`;
}

export function formatDate(value: Date | string, options?: Intl.DateTimeFormatOptions) {
  const date = value instanceof Date ? value : new Date(value);
  if (Number.isNaN(date.getTime())) return "-";
  return new Intl.DateTimeFormat(
    "fa-IR",
    options ?? {
      dateStyle: "medium",
    },
  ).format(date);
}
