import { useEffect, useState } from 'react';
import { api } from '../api/client';
import { useApiRequest } from '../hooks/useApiRequest';
import PageIntro from '../components/PageIntro';
import SearchBox from '../components/SearchBox';
import Pagination from '../components/Pagination';
import { WorkCard } from '../components/Cards';
import { RequestState } from '../components/States';

export default function WorksPage() {
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
    (signal) => api.getWorks({ page, search, signal }),
    [page, search],
  );

  return (
    <>
      <PageIntro eyebrow="کتاب‌ها و مجموعه‌ها" title="آثار و دیوان‌ها" description="مجموعه‌هایی که شعرها در دل آن‌ها گرد آمده‌اند؛ همراه با نام شاعر و توضیح اثر." action={<SearchBox value={searchInput} onChange={setSearchInput} placeholder="جستجوی عنوان اثر یا نام شاعر..." />} />
      <div className="result-summary">{data && <span>{data.count.toLocaleString('fa-IR')} اثر در کتابخانه</span>}</div>
      <RequestState loading={loading} error={error} retry={retry} empty={data?.results.length === 0}>
        <div className="card-grid">{data?.results.map((work) => <WorkCard key={work.id} work={work} />)}</div>
        {data && <Pagination page={page} count={data.count} onChange={setPage} />}
      </RequestState>
    </>
  );
}
