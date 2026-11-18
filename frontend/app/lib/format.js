export function toPersianNumber(value) {
  return new Intl.NumberFormat("fa-IR").format(Number(value) || 0);
}

export function excerpt(value, maxLength = 180) {
  if (!value) return "";
  const text = String(value).replace(/\s+/g, " ").trim();
  if (text.length <= maxLength) return text;
  return `${text.slice(0, maxLength).trimEnd()}…`;
}

export function formatDate(value) {
  if (!value) return "";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "";

  return new Intl.DateTimeFormat("fa-IR", {
    dateStyle: "medium",
    timeZone: "Asia/Tehran",
  }).format(date);
}

export function firstLetter(value) {
  return String(value || "ش").trim().charAt(0) || "ش";
}
