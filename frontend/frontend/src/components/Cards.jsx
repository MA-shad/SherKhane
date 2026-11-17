import { Link } from 'react-router-dom';

function firstCharacter(value) {
  return String(value || '؟').trim().charAt(0) || '؟';
}

export function PoetCard({ poet }) {
  return (
    <article className="entity-card poet-card">
      <div className="poet-card__mark" aria-hidden="true">{firstCharacter(poet.name)}</div>
      <div className="entity-card__body">
        <div className="entity-card__meta">
          <span>{poet.century ? `قرن ${poet.century}` : 'دوره تاریخی نامشخص'}</span>
        </div>
        <h2><Link to={`/poets/${poet.id}`}>{poet.name}</Link></h2>
        <p>{poet.bio || 'زندگی‌نامه‌ای برای این شاعر ثبت نشده است.'}</p>
        <Link className="text-link" to={`/poets/${poet.id}`}>شناخت بیشتر <span aria-hidden="true">←</span></Link>
      </div>
    </article>
  );
}

export function WorkCard({ work }) {
  return (
    <article className="entity-card work-card">
      <div className="book-mark" aria-hidden="true"><span>«</span></div>
      <div className="entity-card__body">
        <p className="eyebrow">اثر ادبی</p>
        <h2><Link to={`/works/${work.id}`}>{work.title}</Link></h2>
        <p className="muted-line">{work.poet_name || 'نام شاعر ثبت نشده'}</p>
        <p>{work.description || 'توضیحی برای این اثر ثبت نشده است.'}</p>
        {work.poet && <Link className="text-link" to={`/poets/${work.poet}`}>صفحه شاعر <span aria-hidden="true">←</span></Link>}
      </div>
    </article>
  );
}

export function PoemCard({ poem }) {
  return (
    <article className="poem-card">
      <div className="poem-card__topline">
        <span>{poem.poem_type || 'قالب نامشخص'}</span>
        {poem.rhythm_name && <span>{poem.rhythm_name}</span>}
      </div>
      <h2><Link to={`/poems/${poem.id}`}>{poem.title}</Link></h2>
      <p className="poem-card__byline">
        {poem.poet && <Link to={`/poets/${poem.poet}`}>{poem.poet_name || 'شاعر نامشخص'}</Link>}
        {!poem.poet && (poem.poet_name || 'شاعر نامشخص')}
        {poem.work_title && <> · {poem.work_title}</>}
      </p>
      <Link className="text-link" to={`/poems/${poem.id}`}>خواندن شعر <span aria-hidden="true">←</span></Link>
    </article>
  );
}
