import { createJsonLd } from "../lib/seo";

export default function JsonLd({ value }) {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: createJsonLd(value) }}
    />
  );
}
