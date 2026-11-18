import { useLoaderData } from "react-router";
import { getWorks } from "../lib/api.server";
import { pageMeta, canonicalLink, getRequestOrigin } from "../lib/seo";
import PageIntro from "../components/PageIntro";
import SearchForm from "../components/SearchForm";
import Pagination from "../components/Pagination";
import { WorkCard } from "../components/Cards";
import { EmptyState, RecordCount } from "../components/States";

export function meta({ data }) {
  const description = "مجموعه‌ها، دیوان‌ها و آثار ادبی ثبت‌شده در کتابخانه شعرخانه را مرور کنید.";
  return pageMeta("آثار و دیوان‌های شاعران", description, "website", data?.origin ? new URL("/works", data.origin).toString() : undefined);
}

export function links() {
  return [];
}

export async function loader({ request }) {
  const url = new URL(request.url);
  const search = url.searchParams.get("search")?.trim() || "";
  const page = Math.max(1, Number.parseInt(url.searchParams.get("page") || "1", 10) || 1);
  const collection = await getWorks({ page, search, signal: request.signal });
  return { ...collection, search, page, origin: getRequestOrigin(request) };
}

export default function WorksPage() {
  const data = useLoaderData();

  return (
    <>
      <PageIntro
        eyebrow="کتاب‌ها و مجموعه‌ها"
        title="آثار ادبی"
        description="دیوان‌ها و مجموعه‌هایی را ببینید که آثار شاعران در آن‌ها گرد آمده‌اند."
        aside={<SearchForm value={data.search} placeholder="عنوان اثر یا نام شاعر" />}
      />
      <div className="list-toolbar">
        <RecordCount count={data.count} />
        {data.search && <p className="active-filter">نتایج جستجو برای «{data.search}»</p>}
      </div>

      {data.results.length ? (
        <div className="card-grid">
          {data.results.map((work) => <WorkCard key={work.id} work={work} />)}
        </div>
      ) : (
        <EmptyState
          title="اثری پیدا نشد"
          description={data.search ? "عبارت دیگری را برای جستجو امتحان کنید." : "هنوز اثری در این بخش ثبت نشده است."}
          actionTo="/works"
          actionLabel="نمایش همه آثار"
        />
      )}

      <Pagination
        page={data.page}
        search={data.search}
        hasNext={Boolean(data.next)}
        hasPrevious={Boolean(data.previous)}
      />
    </>
  );
}
