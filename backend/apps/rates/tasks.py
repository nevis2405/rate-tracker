from django.conf import settings
from celery import shared_task

from apps.rates.services.ingestion import ingest_rates


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={'max_retries': 3})
def ingest_rates_task(self):
    file_path = settings.BASE_DIR / "rates_seed.parquet"

    ingest_rates(str(file_path))