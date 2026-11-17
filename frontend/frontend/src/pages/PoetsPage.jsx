import { useEffect, useState } from 'react';
import { api } from '../api/client';
import { useApiRequest } from '../hooks/useApiRequest';
import PageIntro from '../components/PageIntro';
import SearchBox from '../components/SearchBox';
import Pagination from '../components/Pagination';
import { PoetCard } from '../components/Cards';
import { RequestState } from '../components/States';

export default function PoetsPage() {
  const [searchInput, setSearchInput] = useState('');
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);

  useEffect(() => {
    const timeout = window.setTimeout(() => {
      setPage(1);
      setSearch(searchInput.trim());
    }, 350);
    return () => window.clearTimeout(timeout);
  }, [searchInput]);

  const { data, loading, error, retry } = useApiRequest(
    (signal) => api.getPoets({ page, search, signal }),
    [page, search],
  );

  return (
    <>
      <PageIntro eyebrow="گنجینه‌ی نام‌ها" title="شاعران" description="با زندگی و جهان شاعرانی آشنا شو که زبان فارسی را شکل داده‌اند." action={<SearchBox value={searchInput} onChange={setSearchInput} placeholder="نام شاعر یا بخشی از زندگی‌نامه..." />} />
      <div className="result-summary">{data && <span>{data.count.toLocaleString('fa-IR')} شاعر در کتابخانه</span>}</div>
      <RequestState loading={loading} error={error} retry={retry} empty={data?.results.length === 0}>
        <div className="card-grid">{data?.results.map((poet) => <PoetCard key={poet.id} poet={poet} />)}</div>
        {data && <Pagination page={page} count={data.count} onChange={setPage} />}
      </RequestState>
    </>
  );
}
