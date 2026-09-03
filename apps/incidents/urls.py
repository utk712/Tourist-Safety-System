from django.urls import path
from .views import report_incident

urlpatterns = [
    path("incidents/", report_incident, name="report_incident"),
]