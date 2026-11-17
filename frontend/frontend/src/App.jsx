import { Route, Routes } from 'react-router-dom';
import AppShell from './components/AppShell';
import HomePage from './pages/HomePage';
import PoetsPage from './pages/PoetsPage';
import PoetDetailPage from './pages/PoetDetailPage';
import WorksPage from './pages/WorksPage';
import WorkDetailPage from './pages/WorkDetailPage';
import PoemsPage from './pages/PoemsPage';
import PoemDetailPage from './pages/PoemDetailPage';

function NotFoundPage() {
  return (
    <div className="state-panel state-panel--empty">
      <span className="state-symbol" aria-hidden="true">۴۰۴</span>
      <h1>این صفحه پیدا نشد</h1>
      <p>نشانی واردشده وجود ندارد یا جابه‌جا شده است.</p>
      <a className="button button--dark" href="/">بازگشت به خانه</a>
    </div>
  );
}

export default function App() {
  return (
    <AppShell>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/poets" element={<PoetsPage />} />
        <Route path="/poets/:id" element={<PoetDetailPage />} />
        <Route path="/works" element={<WorksPage />} />
        <Route path="/works/:id" element={<WorkDetailPage />} />
        <Route path="/poems" element={<PoemsPage />} />
        <Route path="/poems/:id" element={<PoemDetailPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </AppShell>
  );
}
