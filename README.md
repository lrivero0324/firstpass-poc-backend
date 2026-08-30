# FirstPass Employer-First Career Platform POC (Backend)

Django REST API for **FirstPass**, a proof of concept for an employer-first career platform where recruiters search candidate profiles and send interview invitations *before* candidates submit traditional applications.

**Companion frontend:** [firstpass-poc-frontend](https://github.com/lrivero0324/firstpass-poc-frontend)

---

## About the app

### Problem
Typical job sites put the burden on applicants: endless applications, little feedback, and employers sorting large piles of poorly matched resumes.

### What this POC proves
The **riskiest technical assumption** of the product: that we can implement employer search + structured, time-sensitive interview invitations + candidate Accept / Save for Later / Decline (with expiration).

### What is included
| Feature | Description |
|--------|-------------|
| Candidate profiles | Skills, experience, education, preferred role, salary floor, work arrangement |
| Employer search / filter | Filter by skill, location, preferred role, work arrangement |
| Interview invitations | Required salary range, work arrangement, role summary, reason for interest |
| Candidate responses | Accept Interview, Save for Later, Decline |
| Expiration | Pending/saved invitations expire after a set number of days |
| Seeded demo data | 2 employers + 6 candidates via `seed_demo` |
| Optional SPA | Built React UI is served from `/` when `frontend_dist/` is present |

### Stack
- Python 3.12
- Django + Django REST Framework
- SQLite locally (optional Postgres via `DATABASE_URL`)
- WhiteNoise + Gunicorn for production

---

## API documentation

Machine-readable endpoint catalog:

- [`api.json`](./api.json) â€” all routes, query params, and request/response shapes

Interactive browsing (when the server is running):

- `http://127.0.0.1:8000/api/` â€” DRF browsable API root
- `http://127.0.0.1:8000/api/health/` â€” health check

---

## Run instructions (local)

### Prerequisites
- Python 3.12+
- pip

### Windows (PowerShell)

```powershell
cd mc6950-rivero-lauren-assignment1.2-backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

### macOS / Linux

```bash
cd mc6950-rivero-lauren-assignment1.2-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

### After starting
| URL | Purpose |
|-----|---------|
| http://127.0.0.1:8000/ | React POC UI (if `frontend_dist/` is present) |
| http://127.0.0.1:8000/api/ | API root |
| http://127.0.0.1:8000/api/health/ | Health check |
| http://127.0.0.1:8000/admin/ | Django admin |

Re-seed demo data anytime:

```bash
python manage.py seed_demo
```

---

## Quick endpoint reference

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/health/` | Service health |
| GET | `/api/candidates/` | List / search candidates |
| GET | `/api/candidates/{id}/` | Candidate detail |
| GET | `/api/employers/` | List demo employers |
| GET | `/api/employers/{id}/` | Employer detail |
| GET | `/api/invitations/` | List invitations |
| GET | `/api/invitations/{id}/` | Invitation detail |
| POST | `/api/invitations/` | Create interview invitation |
| POST | `/api/invitations/{id}/respond/` | Candidate response |

Candidate search query params: `skill`, `location`, `role`, `work_arrangement`, `min_experience`, `max_salary`.

Invitation list filters: `candidate`, `employer`, `status`.

Respond body: `{ "action": "accept" | "save" | "decline" }`.

Full request/response schemas are in [`api.json`](./api.json).

---

## Environment variables

| Variable | Default | Notes |
|----------|---------|--------|
| `SECRET_KEY` | dev insecure key | Required in production |
| `DEBUG` | `True` | Set `False` in production |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated hosts |
| `CORS_ALLOWED_ORIGINS` | localhost Vite ports | Frontend origins |
| `CORS_ALLOW_ALL_ORIGINS` | `False` | Set `True` only if needed |
| `DATABASE_URL` | SQLite file | Optional Postgres URL |

---

## Deploy (Render)

1. Connect this GitHub repo on [Render](https://render.com).
2. Create a **Web Service** (or use `render.yaml`).
3. **Build command:** `pip install -r requirements.txt`
4. **Start command:** `python manage.py migrate --noinput && python manage.py seed_demo && gunicorn config.wsgi:application`
5. Set `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS=.onrender.com`.



## Auto-deploy note

This repository is connected to Vercel for automatic deployments from the `main` branch.

