export interface Permission {
  id: number | string;
  name: string;
  code?: string;
  description?: string;
}

export interface Role {
  id: number | string;
  name: string;
  permissions: Permission[];
}

export interface Branch {
  id: number | string;
  name: string;
  code: string;
  city: string;
  address: string;
  phone?: string;
  managerName?: string;
  status: "active" | "inactive";
  createdAt: string;
}

export interface User {
  id: number | string;
  fullName: string;
  username: string;
  email?: string;
  phone?: string;
  status: "active" | "inactive";
  createdAt: string;
  lastLoginAt?: string;
  role?: Role;
  branch?: Branch;
}

export interface Category {
  id: number | string;
  name: string;
  slug: string;
  description?: string;
  status: "active" | "inactive";
  productsCount?: number;
}

export interface Brand {
  id: number | string;
  name: string;
  slug: string;
  country?: string;
  status: "active" | "inactive";
  productsCount?: number;
}

export interface ProductVariant {
  id: number | string;
  name: string;
  sku: string;
  stock: number;
  attributes?: Record<string, string>;
}

export interface Product {
  id: number | string;
  name: string;
  sku: string;
  barcode?: string;
  categoryId: number | string;
  brandId: number | string;
  purchasePrice: number;
  sellPrice: number;
  stock: number;
  minimumStock: number;
  status: "active" | "inactive";
  category?: Category;
  brand?: Brand;
  variants?: ProductVariant[];
}

export interface Customer {
  id: number | string;
  fullName: string;
  phone: string;
  email?: string;
  branchId?: number | string;
  status: "active" | "inactive";
  balance?: number;
  loyaltyLevel?: string;
  lastPurchaseAt?: string;
  createdAt: string;
}

export interface Supplier {
  id: number | string;
  name: string;
  contactName?: string;
  phone?: string;
  email?: string;
  status: "active" | "inactive";
  leadTimeDays?: number;
  balance?: number;
  lastPurchaseAt?: string;
  createdAt: string;
}

export interface SalesInvoiceItem {
  id?: number | string;
  productId: number | string;
  productName?: string;
  quantity: number;
  unitPrice: number;
  totalPrice: number;
}

export interface SalesInvoice {
  id: number | string;
  number: string;
  branchId: number | string;
  customerId?: number | string;
  date: string;
  totalAmount: number;
  discountAmount?: number;
  paidAmount?: number;
  paymentMethod?: string;
  status: "draft" | "paid" | "partial" | "cancelled";
  items: SalesInvoiceItem[];
}

export interface PurchaseInvoice {
  id: number | string;
  number: string;
  supplierId: number | string;
  branchId?: number | string;
  date: string;
  totalAmount: number;
  paidAmount?: number;
  dueDate?: string;
  status: "pending" | "paid" | "partial" | "cancelled";
}

export interface Account {
  id: number | string;
  code: string;
  name: string;
  type: "asset" | "liability" | "equity" | "income" | "expense";
  balance: number;
  status: "active" | "inactive";
}

export interface JournalEntry {
  id: number | string;
  number: string;
  date: string;
  description?: string;
  debit: number;
  credit: number;
  status: "draft" | "posted";
}

export interface AuditLog {
  id: number | string;
  action: string;
  actorName: string;
  entityType: string;
  entityId?: number | string;
  timestamp: string;
  description?: string;
}

export interface AuthTokens {
  accessToken: string;
  refreshToken?: string;
}

export interface LoginPayload {
  username: string;
  password: string;
}

export interface AuthResponse {
  accessToken?: string;
  refreshToken?: string;
  access_token?: string;
  refresh_token?: string;
  token?: string;
  message?: string;
  user?: User;
}

export interface ApiListEnvelope<T> {
  items?: T[];
  data?: T[];
  results?: T[];
  total?: number;
}

export interface DashboardMetricsResponse {
  todaySales: number;
  customersCount: number;
  lowStockItems: number;
  pendingInstallments: number;
  salesTrend?: Array<{ name: string; sales: number }>;
  recentActivities?: AuditLog[];
}
