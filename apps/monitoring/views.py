import os
import json
import requests
from pathlib import Path
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import SOSAlert
from apps.incidents.models import Incident
from apps.users.models import Tourist

from ai_module.risk_prediction import predict_risk, get_nearest_city
from ai_module.city_coordinates import city_coords

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
    lat = request.GET.get("lat")
    lng = request.GET.get("lng")
    city = request.GET.get("city")
    hour = int(request.GET.get("hour", 20))

    if lat and lng and not city:
        try:
            city = get_nearest_city(float(lat), float(lng))
        except Exception:
            city = "Mumbai"

    if not city:
        city = "Mumbai"

    try:
        risk = predict_risk(
            city=city,
            hour=hour,
            crime_description="Robbery",
            victim_age=30,
            victim_gender="Male",
            weapon_used="Knife",
            crime_domain="Violent Crime",
            crime_count=200
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
        dataset_path = Path(__file__).resolve().parent.parent.parent / "ai_module" / "dataset" / "crime_dataset_india.csv"

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
            except Exception:
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


# 🚓 NEAREST POLICE API (MULTI-PROVIDER FALLBACK: GEOAPIFY + OPENSTREETMAP)
def get_nearest_police(request):
    lat = request.GET.get("lat")
    lng = request.GET.get("lng")

    if not lat or not lng:
        return JsonResponse({"error": "Missing coordinates"})

    try:
        lat = float(lat)
        lng = float(lng)
    except ValueError:
        return JsonResponse({"error": "Invalid coordinates format"})

    result = []
    seen = set()

    # Provider 1: Geoapify Places API (50km radius)
    API_KEY = os.getenv("GEOAPIFY_API_KEY", "69c92f8517d945be9fa04154930985f1")
    url = "https://api.geoapify.com/v2/places"
    params = {
        "categories": "service.police",
        "filter": f"circle:{lng},{lat},50000",
        "bias": f"proximity:{lng},{lat}",
        "limit": 15,
        "apiKey": API_KEY
    }

    try:
        res = requests.get(url, params=params, timeout=8)
        if res.status_code == 200:
            data = res.json()
            for place in data.get("features", []):
                coords = place["geometry"]["coordinates"]
                props = place.get("properties", {})
                p_lat, p_lng = coords[1], coords[0]
                name = props.get("name") or props.get("street") or "Police Station"
                
                dist_m = props.get("distance")
                if dist_m is None:
                    dist_m = math.sqrt((lat - p_lat)**2 + (lng - p_lng)**2) * 111000

                key = (round(p_lat, 4), round(p_lng, 4))
                if key not in seen:
                    seen.add(key)
                    result.append({
                        "lat": p_lat,
                        "lng": p_lng,
                        "name": name,
                        "address": props.get("address_line2") or props.get("city") or props.get("formatted", ""),
                        "distance": round(dist_m / 1000, 2)
                    })
    except Exception:
        pass

    # Provider 2: OpenStreetMap Nominatim Fallback (Free & Global)
    if len(result) < 5:
        try:
            nom_url = "https://nominatim.openstreetmap.org/search"
            headers = {"User-Agent": "SafeGuardAI-TouristSafety/1.0"}
            nom_params = {
                "q": "police station",
                "format": "json",
                "limit": 10,
                "viewbox": f"{lng-0.6},{lat+0.6},{lng+0.6},{lat-0.6}",
                "bounded": 1
            }
            nom_res = requests.get(nom_url, params=nom_params, headers=headers, timeout=8)
            if nom_res.status_code == 200:
                for item in nom_res.json():
                    p_lat = float(item["lat"])
                    p_lng = float(item["lon"])
                    dist_m = math.sqrt((lat - p_lat)**2 + (lng - p_lng)**2) * 111000
                    
                    key = (round(p_lat, 4), round(p_lng, 4))
                    if key not in seen:
                        seen.add(key)
                        result.append({
                            "lat": p_lat,
                            "lng": p_lng,
                            "name": item.get("display_name", "Police Station").split(",")[0],
                            "address": item.get("display_name", ""),
                            "distance": round(dist_m / 1000, 2)
                        })
        except Exception:
            pass

    # Sort by closest distance first
    result.sort(key=lambda x: x["distance"])

    if not result:
        return JsonResponse({"error": "No police stations found nearby. Try searching a major city or dragging the map pin."})

    return JsonResponse(result, safe=False)




# 🤖 AI TOURIST SAFETY ASSISTANT CHATBOT
@csrf_exempt
def ai_chat_assistant(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            msg = data.get("message", "").lower().strip()
            lang = data.get("lang", "en").lower().strip()
        except Exception:
            return JsonResponse({"reply": "Invalid request body format."})

        if not msg:
            return JsonResponse({"reply": "कृपया एक सुरक्षा प्रश्न या गंतव्य पूछताछ टाइप करें!" if lang == "hi" else "Please type a safety question or destination inquiry!"})

        if "police" in msg or "station" in msg or "cop" in msg or "पुलिस" in msg or "थाना" in msg:
            reply = "🚔 निकटतम पुलिस स्टेशन खोजने के लिए [पुलिस खोज](/nearest-police/) का उपयोग करें या 100 / 112 पर कॉल करें।" if lang == "hi" else "🚔 To locate the nearest police stations based on your GPS position, use our [Police Lookup](/nearest-police/) feature or call 100 / 112 immediately."
        elif "sos" in msg or "emergency" in msg or "help" in msg or "danger" in msg or "आपातकाल" in msg or "मदद" in msg or "खतरा" in msg:
            reply = "🚨 यदि आप आपात स्थिति में हैं, तो अपने लाइव जीपीएस स्थान भेजने के लिए [आपातकालीन एसओएस](/sos/) बटन दबाएं या 112 पर कॉल करें!" if lang == "hi" else "🚨 If you are in immediate danger, use the [Emergency SOS](/sos/) button right away to transmit your live GPS coordinates to authorities, or dial 112!"
        elif "night" in msg or "dark" in msg or "late" in msg or "रात" in msg:
            reply = "🌙 यात्रा सुरक्षा सलाह: रात में अंधेरी गलियों से बचें। सत्यापित टैक्सी का उपयोग करें और अपना लाइव स्थान ट्रैकिंग चालू रखें।" if lang == "hi" else "🌙 Safe Travel Tip: Avoid poorly lit alleys late at night. Use verified cabs (Uber/Ola/prepaid taxis), keep your live location tracking ON, and stay near populated areas."
        elif "hospital" in msg or "doctor" in msg or "medical" in msg or "अस्पताल" in msg or "डॉक्टर" in msg:
            reply = "🚑 चिकित्सा आपात स्थिति के लिए तुरंत 108 डायल करें।" if lang == "hi" else "🚑 In case of medical emergencies, dial 108 for an ambulance response. Keep your tourist medical insurance card handy."
        elif "women" in msg or "lady" in msg or "female" in msg or "महिला" in msg or "नारी" in msg:
            reply = "👩 महिला सुरक्षा हेल्पलाइन: आपातकालीन सहायता के लिए 1091 पर कॉल करें।" if lang == "hi" else "👩 Women Safety Helpline: You can reach the dedicated Women Helpline at 1091 anytime for immediate assistance."
        else:
            reply = "🛡️ सेफगार्ड एआई: हमारे डैशबोर्ड पर आप पुलिस स्टेशन, रिस्क स्कोर और टूरिस्ट स्पॉट देख सकते हैं।" if lang == "hi" else "🛡️ SafeGuard AI: You can check live risk scores, nearest police stations, and tourist destinations on our portal."

        return JsonResponse({"reply": reply})

    return JsonResponse({"error": "Method not allowed"}, status=405)



# 🔍 FREE LOCATION SEARCH PROXY (NOMINATIM GEOCODING)
def search_location_api(request):
    query = request.GET.get("q", "").strip()
    if not query:
        return JsonResponse({"error": "Missing query parameter"})

    url = "https://nominatim.openstreetmap.org/search"
    headers = {"User-Agent": "SafeGuardAI-TouristSafety/1.0"}
    params = {
        "q": query,
        "format": "json",
        "limit": 5
    }

    try:
        res = requests.get(url, params=params, headers=headers, timeout=8)
        if res.status_code == 200:
            data = res.json()
            if data:
                return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Location not found"}, status=404)



# 🏛️ ALL-INDIA MONUMENTS & TOURIST SPOTS GUIDE
from .tourist_spots_data import INDIAN_TOURIST_SPOTS, get_all_states, get_all_categories, get_spot_by_id

def tourist_spots(request):
    selected_state = request.GET.get('state', '')
    selected_category = request.GET.get('category', '')
    search_query = request.GET.get('q', '').lower().strip()

    filtered_spots = INDIAN_TOURIST_SPOTS

    if selected_state:
        filtered_spots = [s for s in filtered_spots if s['state'].lower() == selected_state.lower()]

    if selected_category:
        filtered_spots = [s for s in filtered_spots if s['category'].lower() == selected_category.lower()]

    if search_query:
        filtered_spots = [
            s for s in filtered_spots
            if search_query in s['name'].lower()
            or search_query in s['state'].lower()
            or search_query in s['city'].lower()
            or search_query in s['history'].lower()
        ]

    context = {
        "spots": filtered_spots,
        "total_spots_count": len(INDIAN_TOURIST_SPOTS),
        "states": get_all_states(),
        "categories": get_all_categories(),
        "selected_state": selected_state,
        "selected_category": selected_category,
        "search_query": search_query
    }

    return render(request, 'tourist_spots.html', context)


# 🏛️ DEDICATED MONUMENT SHOWCASE & AI AUDIO GUIDE VIEW
def tourist_spot_detail(request, spot_id):
    spot = get_spot_by_id(spot_id)
    if not spot:
        return render(request, 'tourist_spots.html', {'error': 'Monument not found'})

    return render(request, 'tourist_spot_detail.html', {'spot': spot})