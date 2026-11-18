import { getRequestOrigin } from "../lib/seo";

export function loader({ request }) {
  const origin = getRequestOrigin(request);
  const body = [
    "User-agent: *",
    "Allow: /",
    "Disallow: /api/",
    `Sitemap: ${new URL("/sitemap.xml", origin).toString()}`,
    "",
  ].join("\n");

  return new Response(body, {
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "public, max-age=3600",
    },
  });
}
