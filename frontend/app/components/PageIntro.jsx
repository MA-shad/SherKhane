export default function PageIntro({ eyebrow, title, description, aside }) {
  return (
    <header className="page-intro">
      <div className="page-intro__main">
        {eyebrow && <p className="eyebrow">{eyebrow}</p>}
        <h1>{title}</h1>
        {description && <p className="page-intro__description">{description}</p>}
      </div>
      {aside && <div className="page-intro__aside">{aside}</div>}
    </header>
  );
}
