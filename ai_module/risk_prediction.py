import joblib
import pandas as pd


# -------------------------------------
# Load trained model
# -------------------------------------

model = joblib.load("ai_module/risk_model.pkl")

encoder_city = joblib.load("ai_module/encoder_city.pkl")
encoder_crime = joblib.load("ai_module/encoder_crime.pkl")
encoder_gender = joblib.load("ai_module/encoder_gender.pkl")
encoder_weapon = joblib.load("ai_module/encoder_weapon.pkl")
encoder_domain = joblib.load("ai_module/encoder_domain.pkl")
encoder_risk = joblib.load("ai_module/encoder_risk.pkl")


# -------------------------------------
# Safe transform function
# -------------------------------------

def safe_transform(encoder, value):

    if value in encoder.classes_:
        return encoder.transform([value])[0]
    else:
        # unknown value → default
        return 0


# -------------------------------------
# Risk Prediction Function
# -------------------------------------

def predict_risk(
    city,
    hour,
    crime_description,
    victim_age,
    victim_gender,
    weapon_used,
    crime_domain,
    crime_count
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

        return str(e)