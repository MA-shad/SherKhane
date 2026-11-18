import { Link, useLoaderData } from "react-router";
import { getWork } from "../lib/api.server";
import { pageMeta, canonicalLink, createBreadcrumbSchema, getRequestOrigin } from "../lib/seo";
import { excerpt } from "../lib/format";
import Breadcrumbs from "../components/Breadcrumbs";
import JsonLd from "../components/JsonLd";

export async function loader({ params, request }) {
  const work = await getWork(params.workId, { signal: request.signal });
  return { work, origin: getRequestOrigin(request) };
}

export function meta({ data }) {
  if (!data?.work) return pageMeta("جزئیات اثر", "اطلاعات آثار ادبی در شعرخانه.");
  const description = excerpt(data.work.description, 155) || `اطلاعات ${data.work.title} در کتابخانه شعرخانه.`;
  return pageMeta(`${data.work.title}؛ اثر ادبی`, description, "article", new URL(`/works/${data.work.id}`, data.origin).toString());
}

export function links() {
  return [];
}

export default function WorkDetailPage() {
  const { work, origin } = useLoaderData();
  const breadcrumbSchema = createBreadcrumbSchema([
    { name: "خانه", path: "/" },
    { name: "آثار", path: "/works" },
    { name: work.title, path: `/works/${work.id}` },
  ], origin);

  const workSchema = {
    "@context": "https://schema.org",
    "@type": "CreativeWork",
    name: work.title,
    description: work.description || undefined,
    author: work.poet_name ? { "@type": "Person", name: work.poet_name } : undefined,
  };

  return (
    <>
      <JsonLd value={workSchema} />
      <JsonLd value={breadcrumbSchema} />
      <Breadcrumbs items={[
        { label: "خانه", to: "/" },
        { label: "آثار", to: "/works" },
        { label: work.title },
      ]} />

      <article className="reading-page">
        <p className="eyebrow">اثر ادبی</p>
        <h1>{work.title}</h1>
        {work.poet && (
          <p className="reading-page__byline">
            نوشته‌ی <Link to={`/poets/${work.poet}`}>{work.poet_name || "شاعر نامشخص"}</Link>
          </p>
        )}
        <div className="reading-page__rule" />
        <section className="reading-page__description">
          <h2>درباره اثر</h2>
          <p>{work.description || "توضیحی برای این اثر در کتابخانه ثبت نشده است."}</p>
        </section>
        {work.poet && (
          <div className="reading-page__footer">
            <Link className="button button--outline" to={`/poets/${work.poet}`}>بازگشت به صفحه شاعر</Link>
          </div>
        )}
      </article>
    </>
  );
}
