import {
  isRouteErrorResponse,
  Links,
  Meta,
  Outlet,
  Scripts,
  ScrollRestoration,
  useRouteError,
} from "react-router";
import SiteLayout from "./components/SiteLayout";
import "./app.css";

const DEFAULT_DESCRIPTION =
  "شعرخانه؛ کتابخانه‌ای برای شناخت شاعران، مرور آثار و خواندن شعر فارسی.";

export function links() {
  return [
    { rel: "icon", type: "image/svg+xml", href: "/favicon.svg" },
    { rel: "preconnect", href: "https://fonts.googleapis.com" },
    { rel: "preconnect", href: "https://fonts.gstatic.com", crossOrigin: "anonymous" },
    {
      rel: "stylesheet",
      href: "https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700;800&display=swap",
    },
  ];
}

export function meta() {
  return [
    { title: "شعرخانه | خانه‌ای برای شعر فارسی" },
    { name: "description", content: DEFAULT_DESCRIPTION },
    { property: "og:site_name", content: "شعرخانه" },
    { property: "og:locale", content: "fa_IR" },
    { name: "twitter:card", content: "summary" },
  ];
}

export function Layout({ children }) {
  return (
    <html lang="fa" dir="rtl">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="theme-color" content="#f6f3ec" />
        <Meta />
        <Links />
      </head>
      <body>
        {children}
        <ScrollRestoration />
        <Scripts />
      </body>
    </html>
  );
}

export default function App() {
  return (
    <SiteLayout>
      <Outlet />
    </SiteLayout>
  );
}

export function ErrorBoundary() {
  const error = useRouteError();
  const isNotFound = isRouteErrorResponse(error) && error.status === 404;
  const status = isRouteErrorResponse(error) ? error.status : 500;
  const message = isRouteErrorResponse(error)
    ? error.data?.message || error.statusText || "در پردازش درخواست مشکلی پیش آمد."
    : "در ارتباط با سرویس یا پردازش صفحه مشکلی پیش آمد.";

  return (
    <SiteLayout>
      <section className="state-panel state-panel--error" role="alert">
        <span className="state-code">{isNotFound ? "۴۰۴" : String(status)}</span>
        <p className="eyebrow">{isNotFound ? "نشانی نامعتبر" : "خطا در نمایش صفحه"}</p>
        <h1>{isNotFound ? "این صفحه پیدا نشد" : "فعلاً نتوانستیم این صفحه را نمایش دهیم"}</h1>
        <p>{message}</p>
        <a className="button button--dark" href="/">بازگشت به صفحه اصلی</a>
      </section>
    </SiteLayout>
  );
}
