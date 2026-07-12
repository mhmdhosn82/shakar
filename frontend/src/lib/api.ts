import axios from "axios";

const ACCESS_TOKEN_KEY = "shakar.accessToken";

const resolveBaseUrl = () => {
  const configuredBaseUrl = process.env.NEXT_PUBLIC_API_URL?.trim() || "http://127.0.0.1:8000";
  return configuredBaseUrl.replace(/\/+$/, "");
};

export const api = axios.create({
  baseURL: resolveBaseUrl(),
  timeout: 15_000,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = window.localStorage.getItem(ACCESS_TOKEN_KEY);
    if (token) {
      config.headers.Authorization = ["Bearer", token].join(" ");
    }
  }

  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (typeof window !== "undefined" && error?.response?.status === 401) {
      window.localStorage.removeItem(ACCESS_TOKEN_KEY);
      window.localStorage.removeItem("shakar.refreshToken");
      window.localStorage.removeItem("shakar.user");
    }

    return Promise.reject(error);
  },
);
