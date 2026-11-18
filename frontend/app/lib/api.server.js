import "dotenv/config";
import { data } from "react-router";

const API_BASE_URL = (
  process.env.SHERKHANE_API_BASE_URL || "http://127.0.0.1:8000/api"
).replace(/\/+$/, "");

export const PAGE_SIZE = 20;

function getErrorMessage(payload, status) {
  if (payload && typeof payload === "object") {
    if (typeof payload.detail === "string") return payload.detail;

    for (const value of Object.values(payload)) {
      if (typeof value === "string") return value;
      if (Array.isArray(value)) {
        const firstMessage = value.find((item) => typeof item === "string");
        if (firstMessage) return firstMessage;
      }
    }
  }

  if (status === 404) return "مورد درخواستی در شعرخانه پیدا نشد.";
  if (status === 403 || status === 401) return "دسترسی به این اطلاعات مجاز نیست.";
  if (status >= 500) return "سرویس شعرخانه موقتاً با مشکل روبه‌رو شده است.";
  return `درخواست با خطای ${status} روبه‌رو شد.`;
}

function fail(message, status) {
  throw data({ message }, { status });
}

async function request(path, { signal } = {}) {
  let response;

  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
      signal,
    });
  } catch (error) {
    if (error?.name === "AbortError") throw error;
    fail(
      "ارتباط فرانت‌اند با Django برقرار نشد. روشن بودن سرویس backend در Docker و مقدار SHERKHANE_API_BASE_URL را بررسی کن.",
      503,
    );
  }

  if (response.status === 204) return null;

  const contentType = response.headers.get("content-type") || "";
  let payload;

  if (contentType.includes("application/json")) {
    try {
      payload = await response.json();
    } catch {
      fail("پاسخ API معتبر نیست و JSON قابل‌خواندن برنگردانده است.", 502);
    }
  } else {
    const text = await response.text();
    payload = text ? { detail: text.slice(0, 180) } : null;
  }

  if (!response.ok) {
    fail(getErrorMessage(payload, response.status), response.status);
  }

  return payload;
}

function normalizeCollection(payload) {
  if (Array.isArray(payload)) {
    return {
      results: payload,
      count: payload.length,
      next: null,
      previous: null,
    };
  }

  if (payload && Array.isArray(payload.results)) {
    return {
      results: payload.results,
      count: Number.isFinite(payload.count) ? payload.count : payload.results.length,
      next: payload.next ?? null,
      previous: payload.previous ?? null,
    };
  }

  fail("ساختار پاسخ فهرست با Pagination فعلی DRF سازگار نیست.", 502);
}

export async function getCollection(resource, options = {}) {
  const page = Math.max(1, Number.parseInt(options.page, 10) || 1);
  const params = new URLSearchParams();

  if (page > 1) params.set("page", String(page));
  if (typeof options.search === "string" && options.search.trim()) {
    params.set("search", options.search.trim());
  }
  if (typeof options.ordering === "string" && options.ordering.trim()) {
    params.set("ordering", options.ordering.trim());
  }

  const query = params.size ? `?${params.toString()}` : "";
  const payload = await request(`/${resource}/${query}`, {
    signal: options.signal,
  });

  return normalizeCollection(payload);
}

export async function getDetail(resource, id, options = {}) {
  if (!/^\d+$/.test(String(id ?? "")) || Number(id) < 1) {
    fail("شناسه صفحه معتبر نیست.", 404);
  }

  return request(`/${resource}/${id}/`, { signal: options.signal });
}

export const getPoets = (options) => getCollection("poets", options);
export const getPoet = (id, options) => getDetail("poets", id, options);
export const getWorks = (options) => getCollection("works", options);
export const getWork = (id, options) => getDetail("works", id, options);
export const getPoems = (options) => getCollection("poems", options);
export const getPoem = (id, options) => getDetail("poems", id, options);
export const getRhythms = (options) => getCollection("rhythms", options);
