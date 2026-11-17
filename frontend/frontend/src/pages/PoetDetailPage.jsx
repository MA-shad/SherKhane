import { Link, useParams } from 'react-router-dom';
import { api } from '../api/client';
import { useApiRequest } from '../hooks/useApiRequest';
import PageIntro from '../components/PageIntro';
import { PoemCard, WorkCard } from '../components/Cards';
import { RequestState } from '../components/States';

export default function PoetDetailPage() {
  const { id } = useParams();
  const { data, loading, error, retry } = useApiRequest(async (signal) => {
    const poet = await api.getPoet(id, { signal });
    const poems = await api.getPoems({ page: 1, search: poet.name, signal });
    return {
      poet,
      poems: poems.results.filter((poem) => String(poem.poet) === String(poet.id)),
      // PoetSerializer already embeds the poet's WorkSerializer records.
      works: Array.isArray(poet.works) ? poet.works : [],
    };
  }, [id]);

  return (
    <RequestState loading={loading} error={error} retry={retry}>
      {data && <>
        <div className="breadcrumb"><Link to="/poets">شاعران</Link><span>/</span><span>{data.poet.name}</span></div>
        <section className="profile-panel">
          <div className="profile-panel__mark" aria-hidden="true">{data.poet.name?.trim().charAt(0) || 'ش'}</div>
          <div className="profile-panel__content">
            <p className="eyebrow">چهره‌ی ادبی</p>
            <h1>{data.poet.name}</h1>
            <p className="profile-panel__meta">{data.poet.century ? `قرن ${data.poet.century}` : 'دوره تاریخی ثبت نشده'}</p>
            <p className="profile-panel__bio">{data.poet.bio || 'زندگی‌نامه‌ای برای این شاعر ثبت نشده است.'}</p>
          </div>
        </section>

        <section className="section-block">
          <div className="section-heading"><div><p className="eyebrow">کتاب‌ها و مجموعه‌ها</p><h2>آثار {data.poet.name}</h2></div></div>
          {data.works.length ? <div className="card-grid">{data.works.map((work) => <WorkCard key={work.id} work={work} />)}</div> : <p className="subtle-empty">اثری برای این شاعر در صفحه‌ی نخست نتایج پیدا نشد.</p>}
        </section>

        <section className="section-block section-block--tinted">
          <div className="section-heading"><div><p className="eyebrow">از میان سروده‌ها</p><h2>شعرهای {data.poet.name}</h2></div><Link className="text-link" to={`/poems?search=${encodeURIComponent(data.poet.name)}`}>جستجو در همه شعرها <span aria-hidden="true">←</span></Link></div>
          {data.poems.length ? <div className="poem-grid">{data.poems.slice(0, 6).map((poem) => <PoemCard key={poem.id} poem={poem} />)}</div> : <p className="subtle-empty">شعری برای این شاعر در صفحه‌ی نخست نتایج پیدا نشد.</p>}
        </section>
      </>}
    </RequestState>
  );
}
