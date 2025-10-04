from django.db import models
from apps.universe.models import Asset

class FactorMeta(models.Model):
    name = models.CharField(max_length=64, unique=True)
    method = models.CharField(max_length=64, default="custom")
    window = models.IntegerField(default=252)

class FactorValue(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    date = models.DateField()
    name = models.CharField(max_length=64)  # factor name
    value = models.FloatField()
    class Meta:
        unique_together = ("asset", "date", "name")
