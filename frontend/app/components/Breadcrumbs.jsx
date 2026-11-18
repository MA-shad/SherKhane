import { Link } from "react-router";

export default function Breadcrumbs({ items }) {
  return (
    <nav className="breadcrumbs" aria-label="مسیر صفحه">
      {items.map((item, index) => {
        const isLast = index === items.length - 1;
        return (
          <span className="breadcrumbs__item" key={`${item.label}-${index}`}>
            {isLast || !item.to ? (
              <span aria-current={isLast ? "page" : undefined}>{item.label}</span>
            ) : (
              <Link to={item.to}>{item.label}</Link>
            )}
            {!isLast && <span className="breadcrumbs__separator" aria-hidden="true">/</span>}
          </span>
        );
      })}
    </nav>
  );
}
