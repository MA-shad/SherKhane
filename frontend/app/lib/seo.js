const SITE_NAME = "شعرخانه";

export function pageMeta(title, description, type = "website", url = undefined) {
  const fullTitle = title.includes(SITE_NAME) ? title : `${title} | ${SITE_NAME}`;

  return [
    { title: fullTitle },
    { name: "description", content: description },
    { property: "og:type", content: type },
    { property: "og:title", content: fullTitle },
    { property: "og:description", content: description },
    { property: "og:site_name", content: SITE_NAME },
    { property: "og:locale", content: "fa_IR" },
    ...(url ? [
      { property: "og:url", content: url },
      { tagName: "link", rel: "canonical", href: url },
    ] : []),
    { name: "twitter:card", content: "summary" },
    { name: "twitter:title", content: fullTitle },
    { name: "twitter:description", content: description },
  ];
}

export function createJsonLd(value) {
  return JSON.stringify(value)
    .replace(/</g, "\\u003c")
    .replace(/\u2028/g, "\\u2028")
    .replace(/\u2029/g, "\\u2029");
}

export function createBreadcrumbSchema(items, baseUrl) {
  return {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: items.map((item, index) => ({
      "@type": "ListItem",
      position: index + 1,
      name: item.name,
      item: new URL(item.path, baseUrl).toString(),
    })),
  };
}

export function getRequestOrigin(request) {
  const configuredOrigin = process.env.PUBLIC_SITE_URL?.trim();
  if (configuredOrigin) {
    try {
      return new URL(configuredOrigin).origin;
    } catch {
      throw new Error("PUBLIC_SITE_URL باید یک URL معتبر و کامل باشد.");
    }
  }

  return new URL(request.url).origin;
}

export function canonicalLink(origin, path) {
  if (!origin) return [];
  return [{ rel: "canonical", href: new URL(path, origin).toString() }];
}
