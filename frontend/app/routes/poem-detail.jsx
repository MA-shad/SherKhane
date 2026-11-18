import { Link, useLoaderData } from "react-router";
import { getPoem } from "../lib/api.server";
import { pageMeta, canonicalLink, createBreadcrumbSchema, getRequestOrigin } from "../lib/seo";
import { toPersianNumber } from "../lib/format";
import Breadcrumbs from "../components/Breadcrumbs";
import JsonLd from "../components/JsonLd";
import { EmptyState } from "../components/States";

export async function loader({ params, request }) {
  const poem = await getPoem(params.poemId, { signal: request.signal });
  return { poem, origin: getRequestOrigin(request) };
}

export function meta({ data }) {
  if (!data?.poem) return pageMeta("مطالعه شعر", "خواندن شعرهای فارسی در شعرخانه.");
  const byline = data.poem.poet_name ? ` از ${data.poem.poet_name}` : "";
  const description = `${data.poem.title}${byline}؛ متن شعر و اطلاعات ثبت‌شده در کتابخانه شعرخانه.`;
  return pageMeta(`${data.poem.title}؛ متن شعر`, description, "article", new URL(`/poems/${data.poem.id}`, data.origin).toString());
}

export function links() {
  return [];
}

export default function PoemDetailPage() {
  const { poem, origin } = useLoaderData();
  const verses = Array.isArray(poem.verses) ? poem.verses : [];
  const breadcrumbSchema = createBreadcrumbSchema([
    { name: "خانه", path: "/" },
    { name: "اشعار", path: "/poems" },
    { name: poem.title, path: `/poems/${poem.id}` },
  ], origin);

  const poemSchema = {
    "@context": "https://schema.org",
    "@type": "CreativeWork",
    name: poem.title,
    inLanguage: "fa",
    genre: poem.poem_type || undefined,
    author: poem.poet_name ? { "@type": "Person", name: poem.poet_name } : undefined,
    isPartOf: poem.work_title ? { "@type": "CreativeWork", name: poem.work_title } : undefined,
    text: verses.map((verse) => `${verse.first_couplet} ${verse.second_couplet}`).join("\n"),
  };

  return (
    <>
      <JsonLd value={poemSchema} />
      <JsonLd value={breadcrumbSchema} />
      <Breadcrumbs items={[
        { label: "خانه", to: "/" },
        { label: "اشعار", to: "/poems" },
        { label: poem.title },
      ]} />

      <article className="poem-reading">
        <header className="poem-reading__header">
          <p className="eyebrow">متن شعر</p>
          <h1>{poem.title}</h1>
          <div className="poem-reading__metadata">
            {poem.poet && <Link to={`/poets/${poem.poet}`}>{poem.poet_name || "شاعر نامشخص"}</Link>}
            {!poem.poet && poem.poet_name && <span>{poem.poet_name}</span>}
            {poem.work && <Link to={`/works/${poem.work}`}>{poem.work_title || "اثر ادبی"}</Link>}
            {poem.poem_type && <span>{poem.poem_type}</span>}
            {poem.rhythm_name && <span>{poem.rhythm_name}</span>}
          </div>
        </header>

        <div className="poem-reading__body">
          {verses.length ? (
            <ol className="verse-list">
              {verses.map((verse, index) => (
                <li className="verse-couplet" key={verse.id ?? `${verse.order}-${index}`}>
                  <span className="verse-couplet__number" aria-label={`بیت ${verse.order || index + 1}`}>
                    {toPersianNumber(verse.order || index + 1)}
                  </span>
                  <p>{verse.first_couplet}</p>
                  <p>{verse.second_couplet}</p>
                </li>
              ))}
            </ol>
          ) : (
            <EmptyState title="متن ابیات ثبت نشده است" description="اطلاعات این شعر در کتابخانه وجود دارد، اما هنوز بیتی برای نمایش به آن پیوست نشده است." />
          )}
        </div>

        <footer className="poem-reading__footer">
          {poem.poet && <Link className="button button--outline" to={`/poets/${poem.poet}`}>صفحه شاعر</Link>}
          <Link className="text-link" to="/poems">بازگشت به کتابخانه اشعار <span aria-hidden="true">←</span></Link>
        </footer>
      </article>
    </>
  );
}
