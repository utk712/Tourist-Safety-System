from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import json
import requests

from .models import SOSAlert
from apps.incidents.models import Incident
from apps.users.models import Tourist

from ai_module.risk_prediction import predict_risk
from ai_module.city_coordinates import city_coords
from django.views.decorators.csrf import csrf_exempt


crime_data_cache = None


# 🔴 SOS ALERT
def sos_alert(request):

    if request.method == "POST":

        user = request.POST.get("user")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")

        try:
            SOSAlert.objects.create(
                user=user,
                latitude=float(latitude),
                longitude=float(longitude)
            )
        except Exception as e:
            return JsonResponse({"error": str(e)})

        return render(request, "sos_success.html")

    return render(request, "sos.html")


# 📊 DASHBOARD
def dashboard(request):

    tourists = Tourist.objects.all()
    incidents = Incident.objects.all()
    sos_alerts = SOSAlert.objects.all()

    context = {
        "tourists": tourists,
        "incidents": incidents,
        "alerts": sos_alerts
    }

    return render(request, "dashboard.html", context)


# 🤖 AI RISK PREDICTION
def check_location_risk(request):

    city = request.GET.get("city", "Mumbai")
    hour = int(request.GET.get("hour", 20))

    crime_description = "Robbery"
    victim_age = 30
    victim_gender = "Male"
    weapon_used = "Knife"
    crime_domain = "Violent Crime"
    crime_count = 200

    try:
        risk = predict_risk(
            city,
            hour,
            crime_description,
            victim_age,
            victim_gender,
            weapon_used,
            crime_domain,
            crime_count
        )

    except Exception as e:
        return JsonResponse({"error": str(e)})

    return JsonResponse({
        "city": city,
        "risk_level": risk
    })


# 🔥 CRIME HEATMAP DATA
def crime_heatmap_data(request):

    global crime_data_cache

    if crime_data_cache is None:

        dataset_path = "ai_module/dataset/crime_dataset_india.csv"

        try:
            df = pd.read_csv(dataset_path)
            df = df.head(10000)
        except Exception as e:
            return JsonResponse({"error": str(e)})

        heatmap_data = []

        for _, row in df.iterrows():

            city = row.get("City", "")
            coords = city_coords.get(city)

            if not coords:
                continue

            lat, lng = coords

            hour = row.get("Hour", 20)
            crime_description = row.get("Crime Description", "Theft")
            victim_age = row.get("Victim Age", 30)
            victim_gender = row.get("Victim Gender", "Male")
            weapon_used = row.get("Weapon Used", "Knife")
            crime_domain = row.get("Crime Domain", "Violent Crime")
            crime_count = row.get("crime_count", 200)

            try:
                risk = predict_risk(
                    city,
                    hour,
                    crime_description,
                    victim_age,
                    victim_gender,
                    weapon_used,
                    crime_domain,
                    crime_count
                )
            except:
                risk = "Medium"

            heatmap_data.append({
                "lat": float(lat),
                "lng": float(lng),
                "risk": risk
            })

        crime_data_cache = heatmap_data

    return JsonResponse(crime_data_cache, safe=False)


# 🗺️ PAGES
def crime_map(request):
    return render(request, "map_dashboard.html")


def live_risk_page(request):
    return render(request, "live_risk.html")


def live_tracking_page(request):
    return render(request, "live_tracking.html")


def sos_map(request):
    return render(request, "sos_dashboard.html")


def nearest_police(request):
    return render(request, "nearest_police.html")


# 🚑 SOS DATA FOR MAP
def sos_data(request):

    alerts = SOSAlert.objects.all()
    data = []

    for alert in alerts:
        data.append({
            "user": alert.user,
            "lat": float(alert.latitude),
            "lng": float(alert.longitude)
        })

    return JsonResponse(data, safe=False)


# 📡 LIVE LOCATION UPDATE
@csrf_exempt
def update_location(request):

    if request.method == "POST":

        data = json.loads(request.body)

        lat = data.get("lat")
        lng = data.get("lng")

        return JsonResponse({
            "status": "location received",
            "lat": lat,
            "lng": lng
        })


# 🚓 FINAL FIXED NEAREST POLICE API
def get_nearest_police(request):

    lat = request.GET.get("lat")
    lng = request.GET.get("lng")

    if not lat or not lng:
        return JsonResponse({"error": "Missing coordinates"})

    API_KEY = "69c92f8517d945be9fa04154930985f1"  # 🔥 paste here

    url = "https://api.geoapify.com/v2/places"

    params = {
        "categories": "service.police",
        "filter": f"circle:{lng},{lat},5000",
        "limit": 5,
        "apiKey": API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            return JsonResponse({"error": "Geoapify API error"})

        data = response.json()

        result = []

        for place in data.get("features", []):
            coords = place["geometry"]["coordinates"]

            result.append({
                "lat": coords[1],
                "lng": coords[0],
                "name": place["properties"].get("name", "Police Station")
            })

        if not result:
            return JsonResponse({"error": "No police stations found"})

        return JsonResponse(result, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)})