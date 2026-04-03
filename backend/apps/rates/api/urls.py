from django.urls import path
from .views import LatestRatesView, IngestRatesView, RateHistoryView, LoginView

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("latest/", LatestRatesView.as_view(), name="latest-rates"),
    path("ingest/", IngestRatesView.as_view()),
    path("history/", RateHistoryView.as_view()),
]