from django.core.management.base import BaseCommand
from apps.rates.services.ingestion import ingest_rates

class Command(BaseCommand):
    help = "Seed rate data"

    def handle(self, *args, **kwargs):
        file_path = "rates_seed.parquet"
        ingest_rates(file_path)

        self.stdout.write(self.style.SUCCESS("Data ingestion completed"))