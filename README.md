# Rate Tracker

A full-stack application to ingest, store, expose, and visualize financial rate data.

Built using Django, PostgreSQL, Redis, Celery, and Next.js.

---

## 🛠 Tech Stack

### Backend
- Python, Django, DRF
- PostgreSQL
- Redis
- Celery

### Frontend
- Next.js
- React
- Axios
- Chart.js

### Infra
- Docker + docker-compose

---

### Backend
- Parquet-based ingestion (~1M rows)
- PostgreSQL database with unique constraints for deduplication
- Redis caching for latest rates
- Celery worker + beat scheduler for background ingestion
- Token-based authentication for ingestion trigger

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|---------|------------|
| GET | /api/rates/latest/ | Latest rate per provider (cached) |
| GET | /api/rates/history/ | Historical rates with filters |
| POST | /api/rates/ingest/ | Triggers ingestion task (auth required) |

---

### Endpoint Details

#### GET `/api/rates/latest/`
- Returns latest rate per provider
- Optional filter: `?type=`
- Cached in Redis (TTL: 60s)

---

#### GET `/api/rates/history/`
- Returns time-series data
- Filters:
  - `provider`
  - `type`
  - `start_date`
  - `end_date`
- Ordered by latest date
- Pagination recommended (basic implementation present)

---

#### POST `/api/rates/ingest/`
- Requires authentication token
- Triggers Celery ingestion task
- Does NOT accept JSON payload (reads from parquet file internally)

---

## 🎨 Frontend (Next.js)

- Dashboard available at:
http://localhost:3000

- Features:
  - Latest rates table
  - Line chart (history)
  - Filters (provider, type)
  - Auto-refresh (60 seconds)
  - Loading & error states
  - Responsive layout

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/) installed
- Git
- Port availability: `8000` (Django), `3000` (Next.js), `55432` (PostgreSQL), `6379` (Redis)

---

## Project Structure

```
rate-tracker/
├── backend/
│   ├── apps/
│   │   └── rates/
│   │       ├── api/            # Serializers, views, URLs
│   │       ├── management/     # seed_data command
│   │       ├── migrations/
│   │       ├── services/       # Business logic
│   │       ├── tests/
│   │       ├── models.py
│   │       └── tasks.py        # Celery tasks
│   ├── config/
│   │   ├── celery.py
│   │   ├── settings.py
│   │   └── urls.py
│   ├── rates_seed.parquet
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   └── dashboard/
│   ├── components/
│   │   ├── RateChart.tsx
│   │   └── RateTable.tsx
│   └── lib/
│       └── api.ts
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── DECISIONS.md
└── schema.md
```

---

## Environment Setup

Copy `.env.example` to `.env` and fill in values:

```bash
cp .env.example .env
```

> The app will fail fast with a clear error message if any required variable is missing.

---

## How to Run Locally

### 1. Clone the repository

```bash
git clone <repo-url>
cd rate-tracker
```

### 2. Set up environment

```bash
cp .env.example .env
```

### 3. Start all services

```bash
docker-compose up --build
```

This starts: `db` (PostgreSQL), `redis`, `web` (Django on port 8000), `worker` (Celery), `beat` (Celery scheduler), and `frontend` (Next.js on port 3000).

### 4. Seed the database

In a separate terminal, once services are running:

```bash
make seed
```

This runs `python manage.py seed_data` inside the web container, loading `rates_seed.parquet` (~1,000,000 rows) into PostgreSQL.

### 5. Access the dashboard

```
http://localhost:3000
```

Automatically redirects to `/dashboard`.

The Django API is available at:

```
http://localhost:8000/api/
```

---

## How to Run Tests

```bash
make test
```

This runs `pytest` inside the web container. Tests cover:

- Ingestion worker (mocked HTTP, fixture comparison)
- All three API endpoints via DRF test client / pytest-django

---

## Makefile Commands

```bash
make up     # Build and start all services
make down   # Stop all services
make seed   # Load rates_seed.parquet into the database
make test   # Run the full test suite
make logs   # Tail logs from all containers
```

---

## Architectural Notes

**Ingestion strategy:** `bulk_create` with `ignore_conflicts=True` ensures idempotency — re-running `seed_data` on the same file is safe. A unique constraint on `(provider, rate_type, effective_date)` enforces deduplication at the DB level.

**Raw payload storage:** Every ingested record stores the original `raw_payload` (JSON) alongside cleaned fields, allowing failed parses to be replayed without re-fetching source data.

**Caching:** The `/rates/latest/` endpoint is cached in Redis per rate type. Cache is explicitly invalidated on any successful `POST /rates/ingest/` call.

**Scheduler:** Celery beat drives periodic ingestion. The `beat` service runs inside docker-compose alongside the `worker` service.
