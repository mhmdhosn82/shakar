"use client";

import { ChevronLeft, ChevronRight, DatabaseZap } from "lucide-react";
import type { ReactNode } from "react";
import { useMemo, useState } from "react";

import { Button } from "@/components/ui/Button";
import { CardDescription } from "@/components/ui/Card";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { cn, formatNumber } from "@/lib/utils";

export type ColumnDef<T> = {
  key: keyof T | string;
  title: string;
  render?: (value: unknown, row: T, index: number) => ReactNode;
  align?: "right" | "center" | "left";
  className?: string;
};

interface DataTableProps<T> {
  columns: ColumnDef<T>[];
  data: T[];
  pageSize?: number;
  caption?: string;
  loading?: boolean;
  emptyTitle?: string;
  emptyDescription?: string;
}

export function DataTable<T extends { id?: string | number }>({
  columns,
  data,
  pageSize = 8,
  caption,
  loading,
  emptyTitle = "داده‌ای برای نمایش وجود ندارد",
  emptyDescription = "پس از ثبت اطلاعات جدید، رکوردها در این قسمت نمایش داده می‌شوند.",
}: DataTableProps<T>) {
  const [page, setPage] = useState(1);
  const totalPages = Math.max(1, Math.ceil(data.length / pageSize));
  const currentPage = Math.min(page, totalPages);

  const currentRows = useMemo(() => {
    const start = (currentPage - 1) * pageSize;
    return data.slice(start, start + pageSize);
  }, [currentPage, data, pageSize]);

  const startIndex = data.length === 0 ? 0 : (currentPage - 1) * pageSize + 1;
  const endIndex = Math.min(currentPage * pageSize, data.length);

  return (
    <div className="space-y-4">
      {caption ? <CardDescription>{caption}</CardDescription> : null}
      <div className="overflow-hidden rounded-3xl border border-border/70">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-border/70">
            <thead className="bg-slate-50/90 dark:bg-slate-900/80">
              <tr>
                {columns.map((column) => (
                  <th key={String(column.key)} className={cn("whitespace-nowrap px-4 py-4 text-right text-xs font-bold uppercase tracking-wide text-slate-500 dark:text-slate-400", column.align === "center" && "text-center", column.align === "left" && "text-left", column.className)}>
                    {column.title}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-border/60 bg-white dark:bg-slate-950">
              {loading ? (
                <tr>
                  <td colSpan={columns.length} className="px-4 py-16">
                    <div className="flex flex-col items-center gap-3 text-sm text-slate-500">
                      <LoadingSpinner />
                      در حال دریافت اطلاعات...
                    </div>
                  </td>
                </tr>
              ) : data.length === 0 ? (
                <tr>
                  <td colSpan={columns.length} className="px-4 py-16">
                    <div className="flex flex-col items-center gap-3 text-center">
                      <div className="flex h-14 w-14 items-center justify-center rounded-3xl bg-primary/10 text-primary">
                        <DatabaseZap className="h-6 w-6" />
                      </div>
                      <div className="space-y-1">
                        <p className="font-bold text-slate-900 dark:text-white">{emptyTitle}</p>
                        <p className="max-w-md text-sm leading-7 text-slate-500 dark:text-slate-400">{emptyDescription}</p>
                      </div>
                    </div>
                  </td>
                </tr>
              ) : (
                currentRows.map((row, rowIndex) => (
                  <tr key={String(row.id ?? rowIndex)} className="transition hover:bg-primary/5 dark:hover:bg-primary/10">
                    {columns.map((column) => {
                      const key = column.key as keyof T;
                      const value = row[key];
                      return (
                        <td key={String(column.key)} className={cn("px-4 py-4 align-middle text-sm text-slate-600 dark:text-slate-300", column.align === "center" && "text-center", column.align === "left" && "text-left", column.className)}>
                          {column.render ? column.render(value, row, rowIndex) : String(value ?? "-")}
                        </td>
                      );
                    })}
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      <div className="flex flex-col gap-3 rounded-2xl border border-border/70 bg-slate-50/70 px-4 py-3 text-sm text-slate-600 dark:bg-slate-900/60 dark:text-slate-300 md:flex-row md:items-center md:justify-between">
        <span>
          نمایش {formatNumber(startIndex)} تا {formatNumber(endIndex)} از {formatNumber(data.length)} رکورد
        </span>
        <div className="flex items-center gap-2 self-end md:self-auto">
          <Button variant="outline" size="sm" onClick={() => setPage((value) => Math.max(1, value - 1))} disabled={currentPage === 1}>
            <ChevronRight className="h-4 w-4" />
            قبلی
          </Button>
          <span className="rounded-xl bg-white px-3 py-2 text-xs font-bold dark:bg-slate-950">
            صفحه {formatNumber(currentPage)} از {formatNumber(totalPages)}
          </span>
          <Button variant="outline" size="sm" onClick={() => setPage((value) => Math.min(totalPages, value + 1))} disabled={currentPage === totalPages}>
            بعدی
            <ChevronLeft className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}
