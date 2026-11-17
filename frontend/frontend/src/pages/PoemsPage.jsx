import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { api } from '../api/client';
import { useApiRequest } from '../hooks/useApiRequest';
import PageIntro from '../components/PageIntro';
import SearchBox from '../components/SearchBox';
import Pagination from '../components/Pagination';
import { PoemCard } from '../components/Cards';
import { RequestState } from '../components/States';

export default function PoemsPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const initialSearch = searchParams.get('search') || '';
  const [searchInput, setSearchInput] = useState(initialSearch);
  const [search, setSearch] = useState(initialSearch);
  const [page, setPage] = useState(1);

  useEffect(() => {
    const timeout = window.setTimeout(() => {
      const cleanSearch = searchInput.trim();
      setPage(1);
      setSearch(cleanSearch);
      setSearchParams(cleanSearch ? { search: cleanSearch } : {}, { replace: true });
    }, 350);
    return () => window.clearTimeout(timeout);
  }, [searchInput, setSearchParams]);

  const { data, loading, error, retry } = useApiRequest(
    (signal) => api.getPoems({ page, search, signal, ordering: '-created_at' }),
    [page, search],
  );

  return (
    <>
      <PageIntro eyebrow="خواندنی‌های کتابخانه" title="کتابخانه‌ی اشعار" description="شعرها را بر اساس عنوان، نام شاعر یا اطلاعات ثبت‌شده در کتابخانه پیدا کن." action={<SearchBox value={searchInput} onChange={setSearchInput} placeholder="عنوان شعر یا نام شاعر..." />} />
      <div className="result-summary">{data && <span>{data.count.toLocaleString('fa-IR')} شعر در کتابخانه</span>}</div>
      <RequestState loading={loading} error={error} retry={retry} empty={data?.results.length === 0}>
        <div className="poem-grid">{data?.results.map((poem) => <PoemCard key={poem.id} poem={poem} />)}</div>
        {data && <Pagination page={page} count={data.count} onChange={setPage} />}
      </RequestState>
    </>
  );
}
