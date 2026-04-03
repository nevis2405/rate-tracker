import pyarrow.parquet as pq
from apps.rates.models import Rate
from django.utils import timezone
import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)

def read_parquet_in_batches(file_path, batch_size=5000):
    parquet_file = pq.ParquetFile(file_path)

    for batch in parquet_file.iter_batches(batch_size=batch_size):
        yield batch.to_pandas()

def process_batch(df):
    records = []
    success_count = 0
    fail_count = 0

    for row in df.itertuples(index=False):
        try:
            records.append(
                Rate(
                    provider=row.provider,
                    rate_type=row.rate_type,
                    rate_value=row.rate_value,
                    effective_date=row.effective_date,
                    ingested_at=timezone.now(),

                    currency=row.currency,
                    source_url=row.source_url,
                    raw_response_id=row.raw_response_id,

                    raw_payload=row._asdict()
                )
            )
            success_count += 1

        except Exception:
            fail_count += 1
            continue

    try:
        Rate.objects.bulk_create(
            records,
            batch_size=1000,
            ignore_conflicts=True
        )

    except Exception as e:
        logger.error("Bulk insert failed, falling back to row insert", extra={"error": str(e)})

        for record in records:
            try:
                record.save()
            except Exception:
                fail_count += 1

    return success_count, fail_count


def ingest_rates(file_path):
    logger.info("Ingestion started", extra={"file": file_path})

    total_read = 0
    total_success = 0
    total_failed = 0

    try:
        for df in read_parquet_in_batches(file_path):
            batch_size = len(df)

            logger.info(f"Processing batch size: {batch_size}")

            success, failed = process_batch(df)

            total_read += batch_size
            total_success += success
            total_failed += failed

            logger.info(
                f"Batch done | success={success} failed={failed} total_read={total_read}"
            )

        cache.clear()
        logger.info("Cache cleared after ingestion")

        logger.info(
            f"Ingestion completed | read={total_read} success={total_success} failed={total_failed}"
        )

    except Exception:
        logger.exception("Ingestion FAILED")
        raise
