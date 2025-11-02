# Event Management System API (Django REST)

Production-ready REST API for creating, discovering, and managing events, with RSVPs and reviews. Built with Django, Django REST Framework, JWT auth, and django-filter. Ships with SQLite for local development.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Django](https://img.shields.io/badge/Django-5.2-green)
![DRF](https://img.shields.io/badge/DRF-3.16-red)
![License](https://img.shields.io/badge/License-Choose%20one-lightgrey)

## Features

- JWT authentication (access/refresh) using Simple JWT
- Event CRUD with rich filtering, searching, and ordering
- Public/private events with organizer ownership rules
- RSVP management (Going, Maybe, Not Going) with idempotent updates
- Event reviews with 1–5 ratings and comments
- Pagination out of the box (page, page_size)
- Profile model for users (image upload support)

## Tech Stack

- Django 5.2, Django REST Framework 3.16
- djangorestframework-simplejwt for JWT auth
- django-filter for filtering and search
- SQLite for development

## Project Structure

```txt
emsAPI/
├─ emsAPI/                # Django project config
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py
├─ events/                # Events, RSVPs, Reviews app
│  ├─ models.py
│  ├─ serializers.py
│  ├─ permissions.py
│  ├─ views.py
│  └─ urls.py
├─ users/                 # Auth endpoints + user profiles
│  ├─ models.py
│  ├─ serializers.py
│  └─ urls.py
├─ manage.py
├─ requirements.txt
├─ Postman_Guide.md       # Detailed endpoint guide with examples
└─ db.sqlite3             # Dev DB (generated)
```

## Getting Started (Windows)

Prerequisites:
- Python 3.11+ installed and available in PATH

1. Create and activate a virtual environment

```cmd
python -m venv .venv
.venv\Scripts\activate
```

1. Install dependencies

```cmd
pip install --upgrade pip
pip install -r requirements.txt
```

1. Apply migrations and create a superuser (optional but recommended)

```cmd
python manage.py migrate
python manage.py createsuperuser
```

1. Run the development server

```cmd
python manage.py runserver
```

Server runs at: <http://127.0.0.1:8000>

Admin: <http://127.0.0.1:8000/admin/>

## Authentication

Default permission is authenticated for write operations. Event list/retrieve is public; all other actions require a valid JWT access token.

JWT endpoints:
- Obtain: POST `/api/auth/token/` { username, password }
- Refresh: POST `/api/auth/token/refresh/` { refresh }

Send the access token in the Authorization header:

```http
Authorization: Bearer <access_token>
```

## API Endpoints (Summary)

Base URL: `http://127.0.0.1:8000`

Auth

- POST `/api/auth/token/` – obtain JWT (access, refresh)
- POST `/api/auth/token/refresh/` – refresh access token

Events

- GET `/api/events/` – list public events (public); auth users also see private events they can access
- POST `/api/events/` – create event (auth; organizer is current user)
- GET `/api/events/{id}/` – retrieve (public if event is public; otherwise restricted)
- PUT/PATCH `/api/events/{id}/` – update (auth; organizer only)
- DELETE `/api/events/{id}/` – delete (auth; organizer only)
- POST `/api/events/{id}/rsvp/` – create or update current user’s RSVP (auth)
- GET `/api/events/{id}/reviews/` – list reviews for the event (auth)

RSVPs

- GET `/api/rsvps/` – list current user’s RSVPs (auth)
- POST `/api/rsvps/` – create or update RSVP by event id (auth)
- GET `/api/rsvps/{id}/` – retrieve single RSVP (auth; owner)
- PUT/PATCH `/api/rsvps/{id}/` – update status (auth; owner)
- DELETE `/api/rsvps/{id}/` – delete RSVP (auth; owner)

Reviews

- GET `/api/reviews/` – list current user’s reviews (auth)
- POST `/api/reviews/` – create a review (auth)
- GET `/api/reviews/{id}/` – retrieve (auth; owner)
- PUT/PATCH `/api/reviews/{id}/` – update (auth; owner)
- DELETE `/api/reviews/{id}/` – delete (auth; owner)

### Filtering, Search, Ordering (Events)

Parameters supported on `GET /api/events/`:

- `search`: applies to `title`, `description`, `location`, `organizer__username`
- `is_public`: `true` | `false`
- `organizer`: organizer user id
- `ordering`: e.g. `-created_at`, `start_time`, `title`
- Pagination: `page` (page size default 10)

Examples:

```http
GET /api/events/?search=concert&is_public=true&ordering=-start_time
GET /api/events/?organizer=1&page=2
```

### RSVP Status Values

One of: `Going`, `Maybe`, `Not Going`

## Example Requests (curl)

Obtain token:

```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"admin\",\"password\":\"admin\"}"
```

Create event:

```bash
curl -X POST http://127.0.0.1:8000/api/events/ \
  -H "Authorization: Bearer <access>" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Tech Conference 2025\",\"description\":\"Annual technology conference\",\"location\":\"NYC\",\"start_time\":\"2025-02-20T09:00:00Z\",\"end_time\":\"2025-02-20T17:00:00Z\",\"is_public\":true}"
```

RSVP to event:

```bash
curl -X POST http://127.0.0.1:8000/api/events/1/rsvp/ \
  -H "Authorization: Bearer <access>" \
  -H "Content-Type: application/json" \
  -d "{\"status\":\"Going\"}"
```

More examples (including responses) are in `Postman_Guide.md`.

## Data Model (Overview)

- `Event`: title, description, organizer (User), location, start_time, end_time, is_public
- `RSVP`: event, user, status (unique per event+user)
- `Review`: event, user, rating (1–5), comment
- `UserProfile`: full_name, bio, location, profile_picture

Organizer can edit/delete their events; other users have read-only access (public events) or access if invited (private with RSVP).

## Running Tests

```cmd
python manage.py test
```

## Media and File Uploads

User profiles support an optional `profile_picture`. In development (`DEBUG=True`), media is served from:

- MEDIA_URL: `/media/`
- MEDIA_ROOT: `./media/`

## Troubleshooting

- 401 Unauthorized: Ensure you send `Authorization: Bearer <access_token>` and the token isn’t expired.
- 400 Validation Errors: Check `end_time > start_time` for events; review rating must be 1–5; RSVP status must be one of the allowed values.
- Migrations: If you change models, run `python manage.py makemigrations && python manage.py migrate`.
- Pillow: Image fields require Pillow; it’s already in `requirements.txt`.

## Configuration Notes

- Default settings are for development. Update `DEBUG`, `ALLOWED_HOSTS`, `SECRET_KEY` before production.
- Database defaults to SQLite. For Postgres or others, update `DATABASES` in `emsAPI/settings.py`.

## Contributing

1. Fork and create a feature branch
2. Make changes with tests where appropriate
3. Ensure the server runs and tests pass
4. Open a pull request describing your changes

## License

Add your preferred license (e.g., MIT) and include a `LICENSE` file at the repo root.

---

Made with Django REST Framework. See `Postman_Guide.md` for detailed endpoint walkthroughs and sample payloads.

