import { NavLink, Link } from 'react-router-dom';

const navigation = [
  { to: '/poets', label: 'شاعران' },
  { to: '/works', label: 'آثار و دیوان‌ها' },
  { to: '/poems', label: 'کتابخانه اشعار' },
];

export default function AppShell({ children }) {
  return (
    <div className="site-shell">
      <header className="site-header">
        <div className="site-header__inner">
          <Link to="/" className="brand" aria-label="شعرخانه، صفحه اصلی">
            <span className="brand__symbol" aria-hidden="true">ش</span>
            <span className="brand__text"><strong>شعرخانه</strong><small>خانه‌ای برای شعر فارسی</small></span>
          </Link>
          <nav className="main-nav" aria-label="منوی اصلی">
            {navigation.map((item) => (
              <NavLink key={item.to} to={item.to} className={({ isActive }) => isActive ? 'main-nav__link is-active' : 'main-nav__link'}>
                {item.label}
              </NavLink>
            ))}
          </nav>
          <Link to="/poems" className="header-action">رفتن به کتابخانه <span aria-hidden="true">←</span></Link>
        </div>
      </header>

      <main className="main-content">{children}</main>

      <footer className="site-footer">
        <div className="site-footer__inner">
          <div><strong>شعرخانه</strong><p>برای خواندن، شناختن و ماندگار کردن شعر فارسی.</p></div>
          <span>نسخه آزمایشی · داده‌ها از API پروژه دریافت می‌شوند</span>
        </div>
      </footer>
    </div>
  );
}
