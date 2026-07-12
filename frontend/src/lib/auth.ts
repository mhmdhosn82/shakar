import axios from "axios";

import { api } from "@/lib/api";
import type { AuthResponse, LoginPayload, User } from "@/types";

const ACCESS_TOKEN_KEY = "shakar.accessToken";
const REFRESH_TOKEN_KEY = "shakar.refreshToken";
const USER_KEY = "shakar.user";

type BackendCurrentUser = {
  id: string;
  email: string;
  username: string;
  full_name?: string | null;
  phone?: string | null;
  role_id?: string | null;
  branch_id?: string | null;
  created_at: string;
  is_active: boolean;
  is_superuser: boolean;
};

const safeStorage = () => (typeof window === "undefined" ? null : window.localStorage);

const getStoredValue = (key: string) => safeStorage()?.getItem(key) ?? null;

const setStoredValue = (key: string, value: string | null) => {
  const storage = safeStorage();
  if (!storage) return;

  if (value === null) {
    storage.removeItem(key);
    return;
  }

  storage.setItem(key, value);
};

const parseStoredUser = (value: string | null) => {
  if (!value) return null;

  try {
    return JSON.parse(value) as User;
  } catch {
    setStoredValue(USER_KEY, null);
    return null;
  }
};

const mapCurrentUser = (user: BackendCurrentUser): User => ({
  id: user.id,
  email: user.email,
  username: user.username,
  fullName: user.full_name || user.username,
  phone: user.phone || undefined,
  status: user.is_active ? "active" : "inactive",
  createdAt: user.created_at,
  role: user.is_superuser
    ? { id: "admin", name: "مدیر سیستم", permissions: [] }
    : undefined,
});

const normalizeErrorMessage = (error: unknown) => {
  if (!axios.isAxiosError(error)) {
    return "اتصال به سرور برقرار نشد. لطفاً دوباره تلاش کنید.";
  }

  const payload = error.response?.data;
  if (typeof payload?.detail === "string") return payload.detail;
  if (typeof payload?.message === "string") return payload.message;

  if (error.code === "ECONNABORTED") {
    return "پاسخی از سرور دریافت نشد. از اجرای backend مطمئن شوید.";
  }

  if (!error.response) {
    return "اتصال به backend برقرار نشد. آدرس API و اجرای سرور را بررسی کنید.";
  }

  return "ورود به سامانه انجام نشد. لطفاً اطلاعات را بررسی کنید.";
};

export function getToken() {
  return getStoredValue(ACCESS_TOKEN_KEY);
}

export function getStoredUser() {
  return parseStoredUser(getStoredValue(USER_KEY));
}

export function setStoredUser(user: User | null) {
  setStoredValue(USER_KEY, user ? JSON.stringify(user) : null);
}

export async function login(payload: LoginPayload): Promise<AuthResponse> {
  try {
    const { data } = await api.post<AuthResponse>("/api/v1/auth/login", payload);
    const accessToken = data.access_token ?? data.accessToken ?? data.token;
    const refreshToken = data.refresh_token ?? data.refreshToken ?? null;

    if (!accessToken) {
      throw new Error("پاسخ ورود معتبر نبود.");
    }

    setStoredValue(ACCESS_TOKEN_KEY, accessToken);
    setStoredValue(REFRESH_TOKEN_KEY, refreshToken);

    const me = await api.get<BackendCurrentUser>("/api/v1/auth/me");
    const user = mapCurrentUser(me.data);
    setStoredUser(user);

    return {
      ...data,
      accessToken,
      refreshToken: refreshToken ?? undefined,
      user,
    };
  } catch (error) {
    logout();
    throw new Error(normalizeErrorMessage(error));
  }
}

export function logout() {
  setStoredValue(ACCESS_TOKEN_KEY, null);
  setStoredValue(REFRESH_TOKEN_KEY, null);
  setStoredValue(USER_KEY, null);
}
