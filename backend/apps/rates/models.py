from django.db import models

class Rate(models.Model):
    provider = models.CharField(max_length=255)
    rate_type = models.CharField(max_length=100)
    rate_value = models.FloatField()

    effective_date = models.DateField()
    ingested_at = models.DateTimeField(auto_now_add=True)

    currency = models.CharField(max_length=10, null=True, blank=True)
    source_url = models.TextField(null=True, blank=True)
    raw_response_id = models.CharField(max_length=255, null=True, blank=True)
    raw_payload = models.JSONField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["provider", "rate_type", "effective_date"],
                name="unique_rate_record"
            )
        ]