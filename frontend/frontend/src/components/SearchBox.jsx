export default function SearchBox({ value, onChange, placeholder = 'جستجو...' }) {
  return (
    <label className="search-box">
      <span className="search-box__icon" aria-hidden="true">⌕</span>
      <span className="sr-only">جستجو</span>
      <input
        type="search"
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder={placeholder}
        autoComplete="off"
      />
    </label>
  );
}
