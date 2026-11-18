import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("routes/home.jsx"),
  route("poets", "routes/poets.jsx"),
  route("poets/:poetId", "routes/poet-detail.jsx"),
  route("works", "routes/works.jsx"),
  route("works/:workId", "routes/work-detail.jsx"),
  route("poems", "routes/poems.jsx"),
  route("poems/:poemId", "routes/poem-detail.jsx"),
  route("sitemap.xml", "routes/sitemap.jsx"),
  route("robots.txt", "routes/robots.jsx"),
  route("*", "routes/not-found.jsx"),
] satisfies RouteConfig;
