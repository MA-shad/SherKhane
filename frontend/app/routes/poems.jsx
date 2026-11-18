import { useLoaderData } from "react-router";
import { getPoems } from "../lib/api.server";
import { pageMeta, canonicalLink, getRequestOrigin } from "../lib/seo";
import PageIntro from "../components/PageIntro";
import SearchForm from "../components/SearchForm";
import Pagination from "../components/Pagination";
import { PoemCard } from "../components/Cards";
import { EmptyState, RecordCount } from "../components/States";

export function meta({ data }) {
  const description = "شعرهای ثبت‌شده در شعرخانه را بر اساس عنوان یا نام شاعر جستجو کنید و برای خواندن متن کامل هر شعر وارد صفحه آن شوید.";
  return pageMeta("کتابخانه اشعار فارسی", description, "website", data?.origin ? new URL("/poems", data.origin).toString() : undefined);
}

export function links() {
  return [];
}

export async function loader({ request }) {
  const url = new URL(request.url);
  const search = url.searchParams.get("search")?.trim() || "";
  const page = Math.max(1, Number.parseInt(url.searchParams.get("page") || "1", 10) || 1);
  const collection = await getPoems({ page, search, signal: request.signal });
  return { ...collection, search, page, origin: getRequestOrigin(request) };
}

export default function PoemsPage() {
  const data = useLoaderData();

  return (
    <>
      <PageIntro
        eyebrow="خواندن و کشف کردن"
        title="کتابخانه اشعار"
        description="میان شعرهای ثبت‌شده بگردید؛ عنوان شعر، نام شاعر و قالب ادبی را ببینید و متن کامل را بخوانید."
        aside={<SearchForm value={data.search} placeholder="عنوان شعر یا نام شاعر" />}
      />
      <div className="list-toolbar">
        <RecordCount count={data.count} />
        {data.search && <p className="active-filter">نتایج جستجو برای «{data.search}»</p>}
      </div>

      {data.results.length ? (
        <div className="poem-grid">
          {data.results.map((poem) => <PoemCard key={poem.id} poem={poem} />)}
        </div>
      ) : (
        <EmptyState
          title="شعری پیدا نشد"
          description={data.search ? "عبارت دیگری را برای جستجو امتحان کنید." : "هنوز شعری در کتابخانه ثبت نشده است."}
          actionTo="/poems"
          actionLabel="نمایش همه اشعار"
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
