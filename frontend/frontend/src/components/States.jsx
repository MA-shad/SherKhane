export function LoadingState({ label = 'در حال دریافت اطلاعات...' }) {
  return (
    <div className="state-panel" role="status" aria-live="polite">
      <span className="spinner" aria-hidden="true" />
      <p>{label}</p>
    </div>
  );
}

export function ErrorState({ error, onRetry }) {
  return (
    <div className="state-panel state-panel--error" role="alert">
      <span className="state-symbol" aria-hidden="true">!</span>
      <h2>دریافت اطلاعات انجام نشد</h2>
      <p>{error?.message || 'خطای نامشخصی رخ داد.'}</p>
      <button className="button button--dark" type="button" onClick={onRetry}>تلاش دوباره</button>
    </div>
  );
}

export function EmptyState({ title = 'چیزی برای نمایش وجود ندارد', description = 'هنوز داده‌ای برای این بخش ثبت نشده است.' }) {
  return (
    <div className="state-panel state-panel--empty">
      <span className="state-symbol" aria-hidden="true">∅</span>
      <h2>{title}</h2>
      <p>{description}</p>
    </div>
  );
}

export function RequestState({ loading, error, retry, empty, children, loadingLabel }) {
  if (loading) return <LoadingState label={loadingLabel} />;
  if (error) return <ErrorState error={error} onRetry={retry} />;
  if (empty) return <EmptyState />;
  return children;
}
