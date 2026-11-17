# SherKhane Frontend

A small React + Vite frontend for the public reading experience of SherKhane. It consumes the existing Django REST Framework API and does not modify backend code.

## Pages included

- `/` — homepage with live library counts and recent records
- `/poets` — searchable, paginated poet directory
- `/poets/:id` — poet profile, works, and poems
- `/works` — searchable, paginated works/collections
- `/works/:id` — work description and poet details
- `/poems` — searchable, paginated poem library
- `/poems/:id` — poem reading page with ordered couplets

## Requirements

- Node.js 18 or newer
- Django backend running locally
- PostgreSQL configured and migrated as described by the backend project

## Run locally

Terminal 1, start the backend:

```bash
cd backend
python manage.py runserver
```

Terminal 2, start the frontend:

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal (normally `http://127.0.0.1:5173`).

## API configuration

By default, the frontend uses `http://127.0.0.1:8000/api`. To change it, copy `.env.example` to `.env` and edit `VITE_API_BASE_URL`:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

Restart Vite after changing environment variables.

## API contract assumptions

The client supports both raw arrays and DRF page-number pagination (`count`, `next`, `previous`, `results`). It uses the fields currently exposed by the repository's serializers:

- Poet: `id`, `name`, `bio`, `century`, `works`
- Work: `id`, `title`, `poet`, `poet_name`, `description`
- Poem list: `id`, `title`, `poet`, `poet_name`, `work_title`, `rhythm_name`, `poem_type`
- Poem detail: list fields plus `verses`
- Verse: `id`, `order`, `first_couplet`, `second_couplet`

The current Poet serializer does not expose a portrait/image field, so the UI uses a typographic initial instead of inventing a portrait. The current API also does not expose a direct `poet` filter for poems or works; the poet detail page uses DRF search and filters the returned first page by the exact poet ID. A future backend filter (for example `?poet=<id>`) would allow that page to show every related record with proper pagination.

## Scope intentionally not included yet

Authentication UI, user dashboards, online Moshā'ereh, event pages, favorites, and any page whose API has not been implemented are out of scope for this first frontend slice.
