from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination

from apps.rates.models import Rate
from apps.rates.tasks import ingest_rates_task

from .serializers import RateSerializer

from django.db.models import OuterRef, Subquery
from django.core.cache import cache

import logging
logger = logging.getLogger(__name__)

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        token = Token.objects.get(key=response.data["token"])

        return Response({
            "token": token.key,
            "user_id": token.user_id
        })

class LatestRatesView(APIView):

    def get(self, request):
        rate_type = request.query_params.get("type")

        # 🔥 Create cache key
        cache_key = f"latest_rates:{rate_type or 'all'}"

        # 🔥 Try cache
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info("CACHE HIT") 
            return Response(cached_data)
        
        logger.info("CACHE MISS")

        # --- DB QUERY ---
        base_qs = Rate.objects.all()

        if rate_type:
            base_qs = base_qs.filter(rate_type__icontains=rate_type)

        subquery = (
            base_qs.filter(provider=OuterRef("provider"))
            .order_by("-effective_date")
            .values("effective_date")[:1]
        )

        latest_rates = base_qs.filter(
            effective_date=Subquery(subquery)
        )

        serializer = RateSerializer(latest_rates, many=True)
        data = serializer.data

        # Store in cache (TTL = 60 sec)
        cache.set(cache_key, data, timeout=60)

        return Response(data)

class IngestRatesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ingest_rates_task.delay()

        return Response({
            "message": "Ingestion started",
            "status": "processing"
        }, status=status.HTTP_202_ACCEPTED)

class RateHistoryPagination(PageNumberPagination):
    page_size = 30

class RateHistoryView(ListAPIView):
    serializer_class = RateSerializer
    pagination_class = RateHistoryPagination

    def get_queryset(self):
        queryset = Rate.objects.all()

        provider = self.request.query_params.get("provider")
        rate_type = self.request.query_params.get("type")
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if provider:
            queryset = queryset.filter(provider=provider)

        if rate_type:
            queryset = queryset.filter(rate_type__icontains=rate_type)

        if start_date:
            queryset = queryset.filter(effective_date__gte=start_date)

        if end_date:
            queryset = queryset.filter(effective_date__lte=end_date)

        # ✅ CRITICAL FIX (limit data)
        return queryset.order_by("-effective_date")[:100]
