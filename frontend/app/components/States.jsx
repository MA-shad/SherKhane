import { Link } from "react-router";

export function EmptyState({ title, description, actionTo, actionLabel }) {
  return (
    <section className="state-panel" aria-live="polite">
      <span className="state-symbol" aria-hidden="true">∅</span>
      <h2>{title}</h2>
      <p>{description}</p>
      {actionTo && actionLabel && <Link className="text-link" to={actionTo}>{actionLabel} ←</Link>}
    </section>
  );
}

export function RecordCount({ count }) {
  return (
    <p className="record-count">
      {new Intl.NumberFormat("fa-IR").format(count)} مورد در کتابخانه
    </p>
  );
}
