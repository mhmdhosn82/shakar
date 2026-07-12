"use client";

import type { ReactNode } from "react";
import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";

import { getStoredUser, getToken, login as loginRequest, logout as logoutRequest, setStoredUser } from "@/lib/auth";
import type { LoginPayload, User } from "@/types";

interface AuthContextValue {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (payload: LoginPayload) => Promise<User | null>;
  logout: () => void;
  setUser: (user: User | null) => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUserState] = useState<User | null>(null);
  const [token, setTokenState] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setUserState(getStoredUser());
    setTokenState(getToken());
    setIsLoading(false);
  }, []);

  const setUser = useCallback((nextUser: User | null) => {
    setUserState(nextUser);
    setStoredUser(nextUser);
  }, []);

  const login = useCallback(async (payload: LoginPayload) => {
    const response = await loginRequest(payload);
    const nextUser = response.user ?? ({ id: payload.username, fullName: payload.username, username: payload.username, status: "active", createdAt: new Date().toISOString() } as User);
    setUser(nextUser);
    setTokenState(getToken());
    return nextUser;
  }, [setUser]);

  const logout = useCallback(() => {
    setUserState(null);
    setTokenState(null);
    logoutRequest();
  }, []);

  const value = useMemo<AuthContextValue>(() => ({ user, token, isLoading, isAuthenticated: Boolean(token), login, logout, setUser }), [isLoading, login, logout, setUser, token, user]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within an AuthProvider");
  return context;
}
