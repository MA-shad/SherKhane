import { Link, useParams } from 'react-router-dom';
import { api } from '../api/client';
import { useApiRequest } from '../hooks/useApiRequest';
import { RequestState } from '../components/States';

export default function WorkDetailPage() {
  const { id } = useParams();
  const { data, loading, error, retry } = useApiRequest(
    (signal) => api.getWork(id, { signal }),
    [id],
  );

  return (
    <RequestState loading={loading} error={error} retry={retry}>
      {data && <>
        <div className="breadcrumb"><Link to="/works">آثار و دیوان‌ها</Link><span>/</span><span>{data.title}</span></div>
        <article className="work-detail">
          <div className="work-detail__mark" aria-hidden="true">«</div>
          <div>
            <p className="eyebrow">اثر ادبی</p>
            <h1>{data.title}</h1>
            {data.poet && <p className="work-detail__poet">اثرِ <Link to={`/poets/${data.poet}`}>{data.poet_name || 'شاعر نامشخص'}</Link></p>}
            <p className="work-detail__description">{data.description || 'توضیحی برای این اثر ثبت نشده است.'}</p>
            {data.poet && <Link className="button button--dark" to={`/poets/${data.poet}`}>رفتن به صفحه شاعر</Link>}
          </div>
        </article>
      </>}
    </RequestState>
  );
}
