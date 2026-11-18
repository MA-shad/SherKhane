import type { Config } from "@react-router/dev/config";

export default {
  // Render public pages on the server so crawlers receive complete HTML.
  ssr: true,
} satisfies Config;
