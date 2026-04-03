import pytest
from rest_framework.test import APIClient
from apps.rates.models import Rate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
def test_latest_rates():
    Rate.objects.create(
        provider="TestBank",
        rate_type="mortgage",
        rate_value=5.0,
        effective_date="2026-01-01"
    )

    client = APIClient()
    response = client.get("/api/rates/latest/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_history_rates():
    Rate.objects.create(
        provider="TestBank",
        rate_type="mortgage",
        rate_value=5.0,
        effective_date="2026-01-01"
    )

    client = APIClient()
    response = client.get("/api/rates/history/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_ingest_requires_auth():
    client = APIClient()

    response = client.post("/api/rates/ingest/")

    assert response.status_code == 401


@pytest.mark.django_db
def test_ingest_with_auth():
    user = User.objects.create_user(username="test", password="pass")
    token = Token.objects.create(user=user)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    response = client.post("/api/rates/ingest/")

    assert response.status_code == 202