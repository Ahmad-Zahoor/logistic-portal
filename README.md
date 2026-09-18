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

## Project layout

- `logistic_portal/` — Django project settings and root URL config.
- `logistics/` — the app: models, views, forms, admin, templates, and URLs
  for tasks, shipments, vehicles, drivers, and customers.
- `templates/` — shared base template and the login page.
