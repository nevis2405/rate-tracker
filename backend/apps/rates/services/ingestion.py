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

    for row in df.itertuples(index=False):
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

    try:
        Rate.objects.bulk_create(
            records,
            batch_size=1000,
            ignore_conflicts=True
        )
    except Exception as e:
        logger.error("Bulk insert failed, falling back to row insert", extra={"error": str(e)})

        # fallback (row-level safety)
        for record in records:
            try:
                record.save()
            except Exception as row_error:
                logger.error("Row failed", extra={
                    "error": str(row_error),
                    "provider": record.provider
                })

def ingest_rates(file_path):
    logger.info("Ingestion started", extra={"file": file_path})

    total = 0

    try:
        for df in read_parquet_in_batches(file_path):
            batch_size = len(df)

            logger.info(f"Processing batch size: {batch_size}")

            process_batch(df)
            total += batch_size

            logger.info("Batch processed", extra={
                "batch_size": batch_size,
                "total": total
            })

        print(f"TOTAL ROWS READ: {total}")

        cache.clear()
        logger.info("Cache cleared after ingestion")

        logger.info("Ingestion completed", extra={"total_records": total})

    except Exception as e:
        logger.exception("Ingestion FAILED")
        raise
