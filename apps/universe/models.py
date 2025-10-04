from django.db import models

class Asset(models.Model):
    ticker = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=128, blank=True, default="")
    currency = models.CharField(max_length=8, default="KRW")
    sector = models.CharField(max_length=64, null=True, blank=True)
    listed_at = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return self.ticker
