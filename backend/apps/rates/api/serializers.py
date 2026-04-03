from rest_framework import serializers
from apps.rates.models import Rate
import math


class RateSerializer(serializers.ModelSerializer):
    rate_value = serializers.SerializerMethodField()

    class Meta:
        model = Rate
        fields = [
            "provider",
            "rate_type",
            "rate_value",
            "effective_date",
        ]

    def get_rate_value(self, obj):
        value = obj.rate_value

        # Handle NaN safely
        if value is None:
            return None

        if isinstance(value, float) and math.isnan(value):
            return None

        return value