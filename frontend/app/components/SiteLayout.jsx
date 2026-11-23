import { Link, NavLink, useNavigation } from "react-router";

const navigation = [
  { to: "/poets", label: "شاعران" },
  { to: "/works", label: "آثار و دیوان‌ها" },
  { to: "/poems", label: "کتابخانه اشعار" },
  { to: "/games/moshaereh", label: "مشاعره" },
];

export default function SiteLayout({ children }) {
  const navigationState = useNavigation();
  const isNavigating = navigationState.state !== "idle";

  return (
    <div className="site-shell">
      <a className="skip-link" href="#main-content">رفتن به محتوای اصلی</a>

      <header className="site-header">
        <div className="site-header__inner container-wide">
          <Link to="/" className="brand" aria-label="شعرخانه، صفحه اصلی">
            <span className="brand__mark" aria-hidden="true">ش</span>
            <span className="brand__copy">
              <strong>شعرخانه</strong>
              <small>خانه‌ای برای شعر فارسی</small>
            </span>
          </Link>

          <nav className="main-nav" aria-label="منوی اصلی">
            {navigation.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) => `main-nav__link${isActive ? " is-active" : ""}`}
              >
                {item.label}
              </NavLink>
            ))}
          </nav>

          <Link className="header-action" to="/poems">
            خواندن شعر <span aria-hidden="true">←</span>
          </Link>
        </div>
        <div className={`navigation-progress${isNavigating ? " is-visible" : ""}`} aria-hidden="true" />
      </header>

      <main id="main-content" className="main-content">
        <div className="container-wide">{children}</div>
      </main>

      <footer className="site-footer">
        <div className="site-footer__inner container-wide">
          <div>
            <Link to="/" className="footer-brand">شعرخانه</Link>
            <p>برای خواندن، شناختن و ماندگار کردن شعر فارسی.</p>
          </div>
          <div className="footer-links" aria-label="پیوندهای پایانی">
            <Link to="/poets">شاعران</Link>
            <Link to="/works">آثار</Link>
            <Link to="/poems">اشعار</Link>
            <Link to="/games/moshaereh">مشاعره</Link>
          </div>
          <span className="footer-note">محتوا از کتابخانه شعرخانه دریافت می‌شود.</span>
        </div>
      </footer>
    </div>
  );
}
