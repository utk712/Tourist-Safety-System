from django.shortcuts import render
from .models import Incident

def report_incident(request):
    if request.method == "POST":
        tourist_name = request.POST.get("tourist_name")
        description = request.POST.get("description")
        location = request.POST.get("location")

        Incident.objects.create(
            tourist_name=tourist_name,
            description=description,
            location=location
        )

        return render(request, "incidents_success.html")

    return render(request, "incidents.html")