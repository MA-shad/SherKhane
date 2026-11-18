import { data, Link } from "react-router";
import { pageMeta } from "../lib/seo";

export const meta = () => pageMeta("صفحه پیدا نشد", "نشانی درخواستی در شعرخانه پیدا نشد.");

export function loader() {
  throw data({ message: "نشانی واردشده وجود ندارد یا جابه‌جا شده است." }, { status: 404 });
}

export default function NotFoundPage() {
  return (
    <section className="state-panel state-panel--error">
      <span className="state-code">۴۰۴</span>
      <p className="eyebrow">نشانی نامعتبر</p>
      <h1>این صفحه پیدا نشد</h1>
      <p>نشانی واردشده وجود ندارد یا جابه‌جا شده است.</p>
      <Link className="button button--dark" to="/">بازگشت به خانه</Link>
    </section>
  );
}
