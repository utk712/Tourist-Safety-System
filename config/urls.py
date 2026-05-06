from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.users.urls")),
    path("",include("apps.monitoring.urls")),
    path("",include("apps.incidents.urls")),
]