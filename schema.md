# Database Schema

---

## Table: Rate

### Purpose:
Stores financial rate data ingested from parquet file.

---

## Columns

| Column | Type | Description |
|-------|------|------------|
| id | AutoField | Primary key |
| provider | CharField | Provider name |
| rate_type | CharField | Type of rate |
| rate_value | FloatField | Rate value |
| effective_date | DateField | Date of rate |
| ingested_at | DateTimeField | Timestamp of ingestion |
| currency | CharField | Currency (optional) |
| source_url | TextField | Source URL (optional) |
| raw_response_id | CharField | Reference ID (optional) |

---

## Constraints

### Unique Constraint
(provider, rate_type, effective_date)


### Purpose:
- Prevent duplicates
- Ensure idempotency

---

## Indexes (implicit)

- effective_date → for history queries
- provider + rate_type → for filtering

---

## Query Patterns

### 1. Latest rate per provider

Uses subquery:
latest per provider based on effective_date

---

### 2. Historical data

filter by provider + type + date range
order by effective_date

---

### 3. Ingestion tracking

based on ingested_at

---

## Design Decisions

### Single table
- Avoid joins
- Faster reads

---

### FloatField
- Simple storage
- Suitable for display

---

## Trade-offs

| Decision | Trade-off |
|--------|----------|
| FloatField | Precision loss |
| No normalization | Data redundancy |
| No raw storage | No replay capability |

---

## Future Improvements

- Use DecimalField
- Add raw ingestion table
- Add more indexes

---