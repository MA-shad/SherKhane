import { Form, useNavigation } from "react-router";

export default function SearchForm({ value = "", placeholder = "جستجو در کتابخانه..." }) {
  const navigation = useNavigation();
  const isSearching = navigation.state !== "idle";

  return (
    <Form method="get" role="search" className="search-form">
      <label className="sr-only" htmlFor="library-search">عبارت جستجو</label>
      <input
        id="library-search"
        type="search"
        name="search"
        defaultValue={value}
        placeholder={placeholder}
        autoComplete="off"
      />
      <button className="button button--dark" type="submit" disabled={isSearching}>
        {isSearching ? "در حال جستجو…" : "جستجو"}
      </button>
    </Form>
  );
}
