# CRUD_DRF

REST API built with **Django** and **Django REST Framework**, with **JWT authentication**
(SimpleJWT). It manages location records (title, place, city, US state and ZIP code) through a
full set of CRUD endpoints, plus an example of a protected view.

## Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/create/` | Create a record |
| `GET` | `/read/` | List records |
| `POST` | `/update/<id>` | Update a record |
| `DELETE` | `/delete/<id>` | Delete a record |
| `POST` | `/token/` | Get an access/refresh JWT pair |
| `POST` | `/token/refresh/` | Refresh the access token |
| `GET` | `/protegida/` | Example endpoint that requires a valid token |

## Tech stack

- Python · Django 4 · Django REST Framework
- `djangorestframework-simplejwt` for authentication
- Split settings per environment (`settings/base.py`, `dev.py`, `prod.py`)

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # set DJANGO_SECRET_KEY
export DJANGO_SECRET_KEY=change-me
python manage.py migrate
python manage.py runserver
```

**Oscar Cuenca** · [LinkedIn](https://www.linkedin.com/in/ocuenca-moreno/)
