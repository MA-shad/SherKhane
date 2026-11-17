import { Link, useParams } from 'react-router-dom';
import { api } from '../api/client';
import { useApiRequest } from '../hooks/useApiRequest';
import { RequestState } from '../components/States';

export default function PoemDetailPage() {
  const { id } = useParams();
  const { data, loading, error, retry } = useApiRequest(
    (signal) => api.getPoem(id, { signal }),
    [id],
  );

  return (
    <RequestState loading={loading} error={error} retry={retry}>
      {data && <>
        <div className="breadcrumb"><Link to="/poems">کتابخانه اشعار</Link><span>/</span><span>{data.title}</span></div>
        <article className="reading-page">
          <header className="reading-page__header">
            <p className="eyebrow">متن شعر</p>
            <h1>{data.title}</h1>
            <div className="reading-page__metadata">
              {data.poet && <Link to={`/poets/${data.poet}`}>{data.poet_name || 'شاعر نامشخص'}</Link>}
              {!data.poet && <span>{data.poet_name || 'شاعر نامشخص'}</span>}
              {data.work_title && <span>{data.work_title}</span>}
              {data.poem_type && <span>{data.poem_type}</span>}
              {data.rhythm_name && <span>{data.rhythm_name}</span>}
            </div>
          </header>

          {Array.isArray(data.verses) && data.verses.length > 0 ? (
            <div className="verse-list">
              {data.verses.map((verse) => (
                <div className="verse-row" key={verse.id}>
                  <span className="verse-row__number">{Number(verse.order).toLocaleString('fa-IR')}</span>
                  <div className="verse-row__lines">
                    <p>{verse.first_couplet}</p>
                    <p>{verse.second_couplet}</p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="subtle-empty">هنوز بیتی برای این شعر ثبت نشده است.</div>
          )}
        </article>
      </>}
    </RequestState>
  );
}
