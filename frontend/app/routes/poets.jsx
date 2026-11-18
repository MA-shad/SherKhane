import { useLoaderData } from "react-router";
import { getPoets } from "../lib/api.server";
import { pageMeta, canonicalLink, getRequestOrigin } from "../lib/seo";
import PageIntro from "../components/PageIntro";
import SearchForm from "../components/SearchForm";
import Pagination from "../components/Pagination";
import { PoetCard } from "../components/Cards";
import { EmptyState, RecordCount } from "../components/States";

export function meta({ data }) {
  const description = "فهرست شاعران کتابخانه شعرخانه را مرور کنید و برای دیدن زندگی‌نامه و آثار هر شاعر وارد صفحه اختصاصی او شوید.";
  return pageMeta("فهرست شاعران فارسی", description, "website", data?.origin ? new URL("/poets", data.origin).toString() : undefined);
}

export function links() {
  return [];
}

export async function loader({ request }) {
  const url = new URL(request.url);
  const search = url.searchParams.get("search")?.trim() || "";
  const page = Math.max(1, Number.parseInt(url.searchParams.get("page") || "1", 10) || 1);
  const collection = await getPoets({ page, search, signal: request.signal });
  return { ...collection, search, page, origin: getRequestOrigin(request) };
}

export default function PoetsPage() {
  const data = useLoaderData();

  return (
    <>
      <PageIntro
        eyebrow="گنجینه نام‌ها"
        title="شاعران"
        description="با زندگی و جهان شاعرانی آشنا شوید که شعر فارسی را در دوره‌های مختلف شکل داده‌اند."
        aside={<SearchForm value={data.search} placeholder="نام شاعر یا بخشی از زندگی‌نامه" />}
      />

      <div className="list-toolbar">
        <RecordCount count={data.count} />
        {data.search && <p className="active-filter">نتایج جستجو برای «{data.search}»</p>}
      </div>

      {data.results.length ? (
        <div className="card-grid card-grid--poets">
          {data.results.map((poet) => <PoetCard key={poet.id} poet={poet} />)}
        </div>
      ) : (
        <EmptyState
          title="شاعری پیدا نشد"
          description={data.search ? "با عبارت دیگری جستجو کنید یا املای نام را تغییر دهید." : "هنوز اطلاعاتی برای نمایش در این فهرست وجود ندارد."}
          actionTo="/poets"
          actionLabel="نمایش همه شاعران"
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
