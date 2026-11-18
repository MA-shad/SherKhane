import { Link } from "react-router";
import { excerpt, firstLetter } from "../lib/format";

export function PoetCard({ poet }) {
  return (
    <article className="entity-card poet-card">
      <div className="entity-card__mark" aria-hidden="true">{firstLetter(poet.name)}</div>
      <div className="entity-card__content">
        <p className="eyebrow">{poet.century ? `قرن ${poet.century}` : "دوره تاریخی ثبت نشده"}</p>
        <h2><Link to={`/poets/${poet.id}`}>{poet.name}</Link></h2>
        <p className="entity-card__description">
          {excerpt(poet.bio, 150) || "زندگی‌نامه‌ای برای این شاعر ثبت نشده است."}
        </p>
        <Link className="text-link" to={`/poets/${poet.id}`}>شناخت بیشتر <span aria-hidden="true">←</span></Link>
      </div>
    </article>
  );
}

export function WorkCard({ work }) {
  return (
    <article className="entity-card work-card">
      <div className="work-card__mark" aria-hidden="true">«</div>
      <div className="entity-card__content">
        <p className="eyebrow">اثر ادبی</p>
        <h2><Link to={`/works/${work.id}`}>{work.title}</Link></h2>
        <p className="entity-card__byline">
          {work.poet ? <Link to={`/poets/${work.poet}`}>{work.poet_name || "نام شاعر ثبت نشده"}</Link> : "نام شاعر ثبت نشده"}
        </p>
        <p className="entity-card__description">
          {excerpt(work.description, 130) || "توضیحی برای این اثر ثبت نشده است."}
        </p>
      </div>
    </article>
  );
}

export function PoemCard({ poem }) {
  return (
    <article className="poem-card">
      <div className="poem-card__meta">
        <span>{poem.poem_type || "قالب نامشخص"}</span>
        {poem.rhythm_name && <span>{poem.rhythm_name}</span>}
      </div>
      <h2><Link to={`/poems/${poem.id}`}>{poem.title}</Link></h2>
      <p className="poem-card__byline">
        {poem.poet ? (
          <Link to={`/poets/${poem.poet}`}>{poem.poet_name || "شاعر نامشخص"}</Link>
        ) : (
          poem.poet_name || "شاعر نامشخص"
        )}
        {poem.work_title && <span> · {poem.work_title}</span>}
      </p>
      <Link className="text-link" to={`/poems/${poem.id}`}>خواندن شعر <span aria-hidden="true">←</span></Link>
    </article>
  );
}
