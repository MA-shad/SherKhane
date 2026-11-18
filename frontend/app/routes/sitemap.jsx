import { getRequestOrigin } from "../lib/seo";

// The current DRF API is paginated and rate-limited. Until it exposes a
// dedicated sitemap/index endpoint, this sitemap lists public discovery pages.
// Crawlers can discover record pages by following links from those listings.
export function loader({ request }) {
  const origin = getRequestOrigin(request);
  const paths = ["/", "/poets", "/works", "/poems"];
  const entries = paths.map((path) => {
    const location = new URL(path, origin).toString();
    return `<url><loc>${escapeXml(location)}</loc></url>`;
  }).join("");

  const xml = `<?xml version="1.0" encoding="UTF-8"?>` +
    `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${entries}</urlset>`;

  return new Response(xml, {
    headers: {
      "Content-Type": "application/xml; charset=utf-8",
      "Cache-Control": "public, max-age=3600",
    },
  });
}

function escapeXml(value) {
  return value.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&apos;");
}
