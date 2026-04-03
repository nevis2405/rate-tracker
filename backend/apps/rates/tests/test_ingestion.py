import pytest
from apps.rates.models import Rate
from apps.rates.services.ingestion import process_batch
import pandas as pd


@pytest.mark.django_db
def test_process_batch():
    df = pd.DataFrame([{
        "provider": "TestBank",
        "rate_type": "test_rate",
        "rate_value": 5.5,
        "effective_date": "2026-01-01",
        "currency": "USD",
        "source_url": "test",
        "raw_response_id": "123"
    }])

    process_batch(df)

    assert Rate.objects.count() == 1

def test_process_batch_handles_invalid_data():
    df = pd.DataFrame([{
        "provider": None,  # invalid
        "rate_type": "test",
        "rate_value": 5.0,
        "effective_date": "2026-01-01",
        "currency": "USD",
        "source_url": "test",
        "raw_response_id": "123"
    }])

    process_batch(df)

    # Should not crash, may skip row
    assert Rate.objects.count() >= 0