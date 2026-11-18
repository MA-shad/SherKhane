import { Link, useLoaderData } from "react-router";
import { getPoet } from "../lib/api.server";
import { pageMeta, canonicalLink, createBreadcrumbSchema, getRequestOrigin } from "../lib/seo";
import { excerpt, firstLetter, toPersianNumber } from "../lib/format";
import Breadcrumbs from "../components/Breadcrumbs";
import JsonLd from "../components/JsonLd";
import { WorkCard } from "../components/Cards";
import { EmptyState } from "../components/States";

export async function loader({ params, request }) {
  const poet = await getPoet(params.poetId, { signal: request.signal });
  return { poet, origin: getRequestOrigin(request) };
}

export function meta({ data }) {
  if (!data?.poet) return pageMeta("صفحه شاعر", "اطلاعات شاعر در شعرخانه.");
  const description = excerpt(data.poet.bio, 155) || `زندگی‌نامه و آثار ${data.poet.name} در شعرخانه.`;
  return pageMeta(`${data.poet.name}؛ زندگی‌نامه و آثار`, description, "profile", new URL(`/poets/${data.poet.id}`, data.origin).toString());
}

export function links() {
  return [];
}

export default function PoetDetailPage() {
  const { poet, origin } = useLoaderData();
  const works = Array.isArray(poet.works) ? poet.works : [];
  const searchHref = `/poems?search=${encodeURIComponent(poet.name)}`;

  const personSchema = {
    "@context": "https://schema.org",
    "@type": "Person",
    name: poet.name,
    description: poet.bio || undefined,
    jobTitle: "شاعر",
  };

  const breadcrumbSchema = createBreadcrumbSchema([
    { name: "خانه", path: "/" },
    { name: "شاعران", path: "/poets" },
    { name: poet.name, path: `/poets/${poet.id}` },
  ], origin);

  return (
    <>
      <JsonLd value={personSchema} />
      <JsonLd value={breadcrumbSchema} />
      <Breadcrumbs items={[
        { label: "خانه", to: "/" },
        { label: "شاعران", to: "/poets" },
        { label: poet.name },
      ]} />

      <article className="profile-panel">
        <div className="profile-panel__mark" aria-hidden="true">{firstLetter(poet.name)}</div>
        <div className="profile-panel__body">
          <p className="eyebrow">چهره‌ی ادبی</p>
          <h1>{poet.name}</h1>
          <p className="profile-panel__period">
            {poet.century ? `قرن ${toPersianNumber(poet.century)}` : "دوره تاریخی ثبت نشده"}
          </p>
          <div className="profile-panel__bio">
            {poet.bio ? <p>{poet.bio}</p> : <p>زندگی‌نامه‌ای برای این شاعر ثبت نشده است.</p>}
          </div>
          <div className="profile-panel__actions">
            <Link className="button button--dark" to={searchHref}>جستجوی شعرهای این شاعر</Link>
            <span className="profile-panel__count">{toPersianNumber(works.length)} اثر ثبت‌شده</span>
          </div>
        </div>
      </article>

      <section className="content-section">
        <div className="section-heading">
          <div>
            <p className="eyebrow">کتاب‌ها و مجموعه‌ها</p>
            <h2>آثار {poet.name}</h2>
          </div>
        </div>
        {works.length ? (
          <div className="card-grid">
            {works.map((work) => <WorkCard key={work.id} work={work} />)}
          </div>
        ) : (
          <EmptyState title="اثری ثبت نشده است" description="در حال حاضر اثری برای این شاعر در اطلاعات کتابخانه ثبت نشده است." />
        )}
      </section>

      <section className="profile-cta">
        <div>
          <p className="eyebrow">از میان سروده‌ها</p>
          <h2>شعرهای {poet.name} را بخوانید</h2>
          <p>برای دیدن نتیجه‌های مرتبط، جستجوی نام شاعر را در کتابخانه اشعار باز کنید.</p>
        </div>
        <Link className="button button--outline" to={searchHref}>رفتن به شعرها <span aria-hidden="true">←</span></Link>
      </section>
    </>
  );
}
