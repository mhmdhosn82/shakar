"use client";

import { useMutation, useQuery, useQueryClient, type QueryKey } from "@tanstack/react-query";

import { api } from "@/lib/api";
import type { Account, Brand, Branch, Category, Customer, DashboardMetricsResponse, Product, PurchaseInvoice, SalesInvoice, Supplier, User } from "@/types";

const extractList = <T,>(payload: unknown): T[] => {
  if (Array.isArray(payload)) return payload as T[];
  if (payload && typeof payload === "object") {
    const record = payload as Record<string, unknown>;
    for (const key of ["items", "results", "data"]) {
      if (Array.isArray(record[key])) return record[key] as T[];
    }
  }
  return [];
};

const extractObject = <T,>(payload: unknown): T => {
  if (payload && typeof payload === "object" && "data" in (payload as Record<string, unknown>)) {
    const data = (payload as Record<string, unknown>).data;
    if (data && !Array.isArray(data)) return data as T;
  }
  return payload as T;
};

export function useApiList<T>(queryKey: QueryKey, endpoint: string, initialData: T[] = []) {
  return useQuery({
    queryKey,
    queryFn: async () => {
      const { data } = await api.get(endpoint);
      return extractList<T>(data);
    },
    initialData,
  });
}

export function useApiItem<T>(queryKey: QueryKey, endpoint: string, enabled = true) {
  return useQuery({
    queryKey,
    enabled,
    queryFn: async () => {
      const { data } = await api.get(endpoint);
      return extractObject<T>(data);
    },
  });
}

export function useCreateEntity<TInput, TOutput>(endpoint: string, invalidateKeys: QueryKey[] = []) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (payload: TInput) => {
      const { data } = await api.post<TOutput>(endpoint, payload);
      return data;
    },
    onSuccess: async () => {
      await Promise.all(invalidateKeys.map((key) => queryClient.invalidateQueries({ queryKey: key })));
    },
  });
}

export const useDashboardMetrics = () => useApiItem<DashboardMetricsResponse>(["dashboard-metrics"], "/api/v1/dashboard/metrics");
export const useBranches = () => useApiList<Branch>(["branches"], "/api/v1/branches");
export const useUsers = () => useApiList<User>(["users"], "/api/v1/users");
export const useProducts = () => useApiList<Product>(["products"], "/api/v1/products");
export const useCategories = () => useApiList<Category>(["categories"], "/api/v1/categories");
export const useBrands = () => useApiList<Brand>(["brands"], "/api/v1/brands");
export const useCustomers = () => useApiList<Customer>(["customers"], "/api/v1/customers");
export const useSuppliers = () => useApiList<Supplier>(["suppliers"], "/api/v1/suppliers");
export const useSalesInvoices = () => useApiList<SalesInvoice>(["sales-invoices"], "/api/v1/sales/invoices");
export const usePurchaseInvoices = () => useApiList<PurchaseInvoice>(["purchase-invoices"], "/api/v1/purchases/invoices");
export const useAccounts = () => useApiList<Account>(["accounts"], "/api/v1/accounting/accounts");
