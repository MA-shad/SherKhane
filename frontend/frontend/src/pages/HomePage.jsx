import { Link } from 'react-router-dom';
import { api } from '../api/client';
import { useApiRequest } from '../hooks/useApiRequest';
import { ErrorState } from '../components/States';
import { PoetCard, PoemCard } from '../components/Cards';

export default function HomePage() {
  const { data, loading, error, retry } = useApiRequest(async (signal) => {
    const [poets, poems, works] = await Promise.all([
      api.getPoets({ page: 1, signal }),
      api.getPoems({ page: 1, signal }),
      api.getWorks({ page: 1, signal }),
    ]);
    return { poets, poems, works };
  }, []);

  return (
    <>
      <section className="hero-panel">
        <div className="hero-panel__ornament" aria-hidden="true">شعر</div>
        <div className="hero-panel__content">
          <p className="eyebrow eyebrow--light">روایتِ کلمه‌ها</p>
          <h1>هر شعر، دریچه‌ای<br />به جهانی دیگر.</h1>
          <p>در شعرخانه میان شاعران، آثار و بیت‌هایی قدم بزن که بخشی از حافظه‌ی ادبی ما هستند.</p>
          <div className="hero-panel__actions">
            <Link to="/poets" className="button button--light">شناخت شاعران</Link>
            <Link to="/poems" className="hero-text-link">خواندن شعرها <span aria-hidden="true">←</span></Link>
          </div>
        </div>
        <div className="hero-panel__note"><span>کتابخانه‌ی شعر فارسی</span><span>از گذشته تا امروز</span></div>
      </section>

      <section className="home-stats" aria-label="آمار کتابخانه">
        {loading && <p className="muted-line">در حال دریافت آمار کتابخانه...</p>}
        {error && <ErrorState error={error} onRetry={retry} />}
        {data && <>
          <div><strong>{data.poets.count.toLocaleString('fa-IR')}</strong><span>شاعر ثبت‌شده</span></div>
          <div><strong>{data.works.count.toLocaleString('fa-IR')}</strong><span>اثر ادبی</span></div>
          <div><strong>{data.poems.count.toLocaleString('fa-IR')}</strong><span>شعر در کتابخانه</span></div>
        </>}
      </section>

      <section className="section-block">
        <div className="section-heading">
          <div><p className="eyebrow">چهره‌های ادبی</p><h2>در جهان شاعران</h2></div>
          <Link className="text-link" to="/poets">همه شاعران <span aria-hidden="true">←</span></Link>
        </div>
        {loading && <div className="inline-loading">در حال دریافت شاعران...</div>}
        {data && <div className="card-grid card-grid--poets">{data.poets.results.slice(0, 3).map((poet) => <PoetCard key={poet.id} poet={poet} />)}</div>}
      </section>

      <section className="section-block section-block--tinted">
        <div className="section-heading">
          <div><p className="eyebrow">برای خواندن</p><h2>چند شعر از کتابخانه</h2></div>
          <Link className="text-link" to="/poems">همه شعرها <span aria-hidden="true">←</span></Link>
        </div>
        {loading && <div className="inline-loading">در حال دریافت شعرها...</div>}
        {data && <div className="poem-grid">{data.poems.results.slice(0, 3).map((poem) => <PoemCard key={poem.id} poem={poem} />)}</div>}
      </section>
    </>
  );
}
