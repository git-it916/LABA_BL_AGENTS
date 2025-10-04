from django.db import models
from apps.universe.models import Asset

class BLRun(models.Model):
    as_of = models.DateField()
    benchmark = models.CharField(max_length=64)
    tau = models.FloatField(default=0.05)
    delta = models.FloatField(default=2.5)
    method_cov = models.CharField(max_length=64, default="ledoit")
    note = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

class PosteriorWeight(models.Model):
    run = models.ForeignKey(BLRun, on_delete=models.CASCADE, related_name="weights")
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    weight = models.FloatField()
    class Meta:
        unique_together = ("run", "asset")
