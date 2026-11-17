const configuredBase = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api';
export const API_BASE_URL = configuredBase.replace(/\/+$/, '');

export class ApiError extends Error {
  constructor(message, { status = 0, details = null } = {}) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.details = details;
  }
}

function explainError(status, payload) {
  if (status === 404) return 'مورد درخواستی پیدا نشد.';
  if (status === 401 || status === 403) return 'دسترسی به این بخش مجاز نیست.';
  if (status >= 500) return 'سرور هنگام پردازش درخواست با مشکل روبه‌رو شد.';
  if (payload && typeof payload === 'object') {
    const firstValue = Object.values(payload).flat().find((value) => typeof value === 'string');
    if (firstValue) return firstValue;
  }
  return `درخواست با وضعیت ${status} ناموفق بود.`;
}

async function request(path, { signal, ...options } = {}) {
  const url = path.startsWith('http') ? path : `${API_BASE_URL}${path.startsWith('/') ? path : `/${path}`}`;
  let response;

  try {
    response = await fetch(url, {
      ...options,
      signal,
      headers: {
        Accept: 'application/json',
        ...(options.body ? { 'Content-Type': 'application/json' } : {}),
        ...options.headers,
      },
    });
  } catch (error) {
    if (error.name === 'AbortError') throw error;
    throw new ApiError('ارتباط با سرور برقرار نشد. روشن بودن Django و تنظیم بودن آدرس API را بررسی کن.');
  }

  if (response.status === 204) return null;

  const contentType = response.headers.get('content-type') || '';
  let payload;
  if (contentType.includes('application/json')) {
    try {
      payload = await response.json();
    } catch {
      throw new ApiError('پاسخ سرور JSON معتبر نیست.', { status: response.status });
    }
  } else {
    const bodyText = await response.text();
    payload = bodyText ? { detail: bodyText.slice(0, 180) } : null;
  }

  if (!response.ok) {
    throw new ApiError(explainError(response.status, payload), {
      status: response.status,
      details: payload,
    });
  }

  return payload;
}

function normalizeCollection(payload) {
  if (Array.isArray(payload)) {
    return { results: payload, count: payload.length, next: null, previous: null };
  }

  if (payload && Array.isArray(payload.results)) {
    return {
      results: payload.results,
      count: Number.isFinite(payload.count) ? payload.count : payload.results.length,
      next: payload.next ?? null,
      previous: payload.previous ?? null,
    };
  }

  throw new ApiError('ساختار پاسخ فهرست با فرمت مورد انتظار فرانت‌اند سازگار نیست.');
}

function buildQuery({ page = 1, search = '', ordering = '' } = {}) {
  const params = new URLSearchParams();
  if (page > 1) params.set('page', String(page));
  if (search.trim()) params.set('search', search.trim());
  if (ordering) params.set('ordering', ordering);
  const query = params.toString();
  return query ? `?${query}` : '';
}

async function getCollection(resource, options = {}) {
  const payload = await request(`/${resource}/${buildQuery(options)}`, { signal: options.signal });
  return normalizeCollection(payload);
}

async function getDetail(resource, id, { signal } = {}) {
  if (!id || !/^\d+$/.test(String(id))) {
    throw new ApiError('شناسه درخواستی معتبر نیست.', { status: 400 });
  }
  return request(`/${resource}/${id}/`, { signal });
}

export const api = {
  getPoets: (options = {}) => getCollection('poets', options),
  getPoet: (id, options = {}) => getDetail('poets', id, options),
  getWorks: (options = {}) => getCollection('works', options),
  getWork: (id, options = {}) => getDetail('works', id, options),
  getPoems: (options = {}) => getCollection('poems', options),
  getPoem: (id, options = {}) => getDetail('poems', id, options),
  getRhythms: (options = {}) => getCollection('rhythms', options),
};
