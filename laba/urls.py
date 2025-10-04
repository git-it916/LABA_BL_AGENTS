from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/bl/", include("apps.bl.urls")),
    path("api/backtest/", include("apps.backtest.urls")),
]
