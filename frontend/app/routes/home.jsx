import { Link } from "react-router";
import { getPoems, getPoets, getWorks } from "../lib/api.server";
import { pageMeta, canonicalLink, getRequestOrigin } from "../lib/seo";
import { toPersianNumber } from "../lib/format";
import { PoetCard, PoemCard } from "../components/Cards";
import { EmptyState } from "../components/States";

export function meta({ data }) {
  const description = "در شعرخانه شاعران فارسی‌زبان را بشناسید، آثار و دیوان‌ها را مرور کنید و شعرها را با اطلاعات کتابخانه بخوانید.";
  return pageMeta("خانه‌ای برای شعر فارسی", description, "website", data?.origin ? new URL("/", data.origin).toString() : undefined);
}

export function links() {
  return [];
}

export async function loader({ request }) {
  const [poets, works, poems] = await Promise.all([
    getPoets({ page: 1, signal: request.signal }),
    getWorks({ page: 1, signal: request.signal }),
    getPoems({ page: 1, signal: request.signal }),
  ]);

  return { poets, works, poems, origin: getRequestOrigin(request) };
}

export default function HomePage({ loaderData }) {
  const { poets, works, poems } = loaderData;

  return (
    <>
      <section className="hero-panel">
        <div className="hero-panel__ornament" aria-hidden="true">شعر</div>
        <div className="hero-panel__content">
          <p className="eyebrow eyebrow--light">روایتِ کلمه‌ها</p>
          <h1>هر شعر، دریچه‌ای<br />به جهانی دیگر.</h1>
          <p className="hero-panel__description">
            میان شاعران، آثار و بیت‌هایی قدم بزن که بخشی از حافظه‌ی ادبی فارسی‌اند.
          </p>
          <div className="hero-panel__actions">
            <Link className="button button--light" to="/poets">شناخت شاعران</Link>
            <Link className="hero-panel__link" to="/poems">رفتن به کتابخانه اشعار <span aria-hidden="true">←</span></Link>
          </div>
        </div>
        <div className="hero-panel__footnote">
          <span>کتابخانه شعر فارسی</span>
          <span>از گذشته تا امروز</span>
        </div>
      </section>

      <section className="library-stats" aria-label="آمار کتابخانه">
        <div className="library-stat">
          <strong>{toPersianNumber(poets.count)}</strong>
          <span>شاعر ثبت‌شده</span>
        </div>
        <div className="library-stat">
          <strong>{toPersianNumber(works.count)}</strong>
          <span>اثر ادبی</span>
        </div>
        <div className="library-stat">
          <strong>{toPersianNumber(poems.count)}</strong>
          <span>شعر در کتابخانه</span>
        </div>
      </section>

      <section className="content-section">
        <div className="section-heading">
          <div>
            <p className="eyebrow">چهره‌های ادبی</p>
            <h2>در جهان شاعران</h2>
          </div>
          <Link className="text-link" to="/poets">همه شاعران <span aria-hidden="true">←</span></Link>
        </div>
        {poets.results.length ? (
          <div className="card-grid card-grid--poets">
            {poets.results.slice(0, 3).map((poet) => <PoetCard key={poet.id} poet={poet} />)}
          </div>
        ) : (
          <EmptyState title="هنوز شاعری ثبت نشده است" description="پس از افزودن اطلاعات به کتابخانه، شاعران اینجا نمایش داده می‌شوند." />
        )}
      </section>

      <section className="content-section content-section--tinted">
        <div className="section-heading">
          <div>
            <p className="eyebrow">برای خواندن</p>
            <h2>چند شعر از کتابخانه</h2>
          </div>
          <Link className="text-link" to="/poems">همه شعرها <span aria-hidden="true">←</span></Link>
        </div>
        {poems.results.length ? (
          <div className="poem-grid">
            {poems.results.slice(0, 3).map((poem) => <PoemCard key={poem.id} poem={poem} />)}
          </div>
        ) : (
          <EmptyState title="هنوز شعری ثبت نشده است" description="با وارد شدن اشعار به پایگاه داده، تازه‌ترین موارد در این بخش دیده می‌شوند." />
        )}
      </section>
    </>
  );
}
