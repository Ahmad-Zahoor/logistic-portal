# Logistic Portal

A Django web app for running the day-to-day operations of a small logistics
business: tasks, shipments, vehicles, drivers, and customers, all in one
dashboard.

## Features

- **Dashboard** — today's tasks, overdue tasks, active shipments, and
  fleet/driver availability at a glance.
- **Tasks** — daily to-dos (pickup, delivery, maintenance, other) with
  priority, due date, status, and optional links to a shipment/driver.
- **Shipments** — track origin/destination, assigned vehicle & driver,
  status (pending → picked up → in transit → delivered), and notes.
- **Vehicles & Drivers** — fleet and staff records with availability status.
- **Customers** — basic customer records linked to their shipments.
- Full CRUD (create/read/update/delete) for every model, plus the Django
  admin for bulk management.
- Login-protected — every page requires authentication.

## Getting started

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` and log in with the superuser account you
created (or manage records directly at `/admin/`).

## Deploying to Render

This repo includes a `render.yaml` blueprint, `build.sh`, and
production-ready settings (env-driven `SECRET_KEY`/`DEBUG`/`ALLOWED_HOSTS`,
Postgres via `DATABASE_URL`, static files via WhiteNoise, gunicorn as the
app server).

1. Push this repo to GitHub (already done if you're reading this on the
   deployed branch).
2. In the [Render dashboard](https://dashboard.render.com/), click
   **New > Blueprint**, connect your GitHub account, and select this repo.
   Render reads `render.yaml` and provisions a free web service plus a free
   Postgres database automatically.
3. Click **Apply** — Render builds with `build.sh` (installs deps, runs
   `collectstatic` and `migrate`) and starts the app with gunicorn.
4. Once deployed, open a **Shell** for the web service in the Render
   dashboard and run `python manage.py createsuperuser` to create your
   login.
5. Visit the `*.onrender.com` URL Render gives you and log in.

Free-tier Render web services spin down after inactivity and take ~30–60s
to wake back up on the next request — upgrade the plan in `render.yaml` if
you need it always-on.

## Project layout

- `logistic_portal/` — Django project settings and root URL config.
- `logistics/` — the app: models, views, forms, admin, templates, and URLs
  for tasks, shipments, vehicles, drivers, and customers.
- `templates/` — shared base template and the login page.
- `render.yaml`, `build.sh` — Render deployment blueprint and build script.
