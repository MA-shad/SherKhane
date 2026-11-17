export default function Pagination({ page, count, pageSize = 20, onChange }) {
  const totalPages = Math.max(1, Math.ceil(count / pageSize));
  if (totalPages <= 1) return null;

  return (
    <nav className="pagination" aria-label="صفحه‌بندی">
      <button type="button" className="button button--outline" disabled={page <= 1} onClick={() => onChange(page - 1)}>
        قبلی
      </button>
      <span>صفحه {page.toLocaleString('fa-IR')} از {totalPages.toLocaleString('fa-IR')}</span>
      <button type="button" className="button button--outline" disabled={page >= totalPages} onClick={() => onChange(page + 1)}>
        بعدی
      </button>
    </nav>
  );
}
