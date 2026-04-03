## 1. Django + DRF

Chosen for:
- Rapid API development
- Built-in ORM
- Easy integration with PostgreSQL

---

## 2. PostgreSQL

Used because:
- Strong support for analytical queries
- Efficient indexing
- Handles large datasets

---

## 3. Celery + Redis

Used for:
- Background ingestion
- Asynchronous processing
- Scheduled execution via Celery Beat

### Why not cron?
- cron doesn't integrate well with docker-compose
- Celery provides retry + async execution

---

## 4. Redis Caching

Used for:
GET /rates/latest

### Strategy:
- Cache key: `latest_rates:{type}`
- TTL: 60 seconds
- Cache cleared after ingestion

---

## 5. Idempotency

Achieved via:
- DB unique constraint:
(provider, rate_type, effective_date)
- `bulk_create(ignore_conflicts=True)`

This ensures:
- Duplicate rows are skipped
- Re-running ingestion is safe

---

## 6. Query Strategy

Latest rates:
- Uses Django Subquery
- Efficient DB-level filtering

History:
- Filtered via query params
- Ordered by date

---

## 7. Frontend Choice

Next.js chosen for:
- Simplicity
- Good React support
- Easy routing

---

## 8. Charting

Chart.js used for:
- Lightweight implementation
- Simple integration

---

## 9. Auto Refresh

Implemented using: 
setInterval(60000)

---

## 10. Environment Variables

Used for:

DB config
Redis config
Secret key

Fail-fast implemented:
    App crashes if env missing

---

## 11. Docker

All services run via:
docker-compose up

Includes:
- web (Django)
- db (PostgreSQL)
- redis
- worker
- beat

---

## 12. Trade offs

| Decision | Trade-off |
|----------|-----------|
| FloatField | Less precision |
| No normalization | Simpler queries |
| No raw payload storage | Cannot replay raw ingestion |

---

## 13. Future Improvements

- Add raw payload storage
- Use DecimalField
- Add WebSocket updates
- Improve validation

---