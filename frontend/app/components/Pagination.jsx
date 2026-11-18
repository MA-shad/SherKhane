import { Link } from "react-router";

function pageHref(page, search) {
  const params = new URLSearchParams();
  if (page > 1) params.set("page", String(page));
  if (search) params.set("search", search);
  const query = params.toString();
  return query ? `?${query}` : "?";
}

export default function Pagination({ page, search, hasNext, hasPrevious }) {
  if (!hasNext && !hasPrevious) return null;

  return (
    <nav className="pagination" aria-label="صفحه‌بندی نتایج">
      {hasPrevious ? (
        <Link className="button button--outline" to={pageHref(page - 1, search)} rel="prev">
          <span aria-hidden="true">→</span> صفحه قبل
        </Link>
      ) : <span />}
      <span className="pagination__current">صفحه {new Intl.NumberFormat("fa-IR").format(page)}</span>
      {hasNext ? (
        <Link className="button button--outline" to={pageHref(page + 1, search)} rel="next">
          صفحه بعد <span aria-hidden="true">←</span>
        </Link>
      ) : <span />}
    </nav>
  );
}
