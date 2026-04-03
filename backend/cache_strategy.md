# Cache Strategy

## Endpoint
GET /rates/latest

## Cache Key Pattern
latest_rates:{type}

## Invalidation Strategy
- Cache is cleared after ingestion using cache.clear()

## TTL
60 seconds

## Future Improvement
- Instead of clearing all cache, selectively delete:
  - latest_rates:all
  - latest_rates:mortgage
