import joblib
import math
import pandas as pd
from pathlib import Path
from .city_coordinates import city_coords

# -------------------------------------
# Load trained model with robust relative pathing
# -------------------------------------

BASE_DIR = Path(__file__).resolve().parent

model = joblib.load(BASE_DIR / "risk_model.pkl")

encoder_city = joblib.load(BASE_DIR / "encoder_city.pkl")
encoder_crime = joblib.load(BASE_DIR / "encoder_crime.pkl")
encoder_gender = joblib.load(BASE_DIR / "encoder_gender.pkl")
encoder_weapon = joblib.load(BASE_DIR / "encoder_weapon.pkl")
encoder_domain = joblib.load(BASE_DIR / "encoder_domain.pkl")
encoder_risk = joblib.load(BASE_DIR / "encoder_risk.pkl")


# -------------------------------------
# Safe transform function
# -------------------------------------

def safe_transform(encoder, value):
    if value in encoder.classes_:
        return encoder.transform([value])[0]
    else:
        return 0


# -------------------------------------
# Nearest City Lookup by Coordinates
# -------------------------------------

def get_nearest_city(lat, lng):
    min_dist = float("inf")
    nearest_city = "Mumbai"

    for city, (c_lat, c_lng) in city_coords.items():
        dist = math.sqrt((lat - c_lat) ** 2 + (lng - c_lng) ** 2)
        if dist < min_dist:
            min_dist = dist
            nearest_city = city

    return nearest_city


# -------------------------------------
# Risk Prediction Function
# -------------------------------------

def predict_risk(
    city,
    hour,
    crime_description="Theft",
    victim_age=30,
    victim_gender="Male",
    weapon_used="None",
    crime_domain="General",
    crime_count=100
):
    try:
        city_encoded = safe_transform(encoder_city, city)
        crime_encoded = safe_transform(encoder_crime, crime_description)
        gender_encoded = safe_transform(encoder_gender, victim_gender)
        weapon_encoded = safe_transform(encoder_weapon, weapon_used)
        domain_encoded = safe_transform(encoder_domain, crime_domain)

        data = pd.DataFrame(
            [[
                city_encoded,
                hour,
                crime_encoded,
                victim_age,
                gender_encoded,
                weapon_encoded,
                domain_encoded,
                crime_count
            ]],
            columns=[
                "City",
                "Hour",
                "Crime Description",
                "Victim Age",
                "Victim Gender",
                "Weapon Used",
                "Crime Domain",
                "crime_count"
            ]
        )

        prediction = model.predict(data)
        risk_label = encoder_risk.inverse_transform(prediction)

        return risk_label[0]

    except Exception as e:
        return "Medium"