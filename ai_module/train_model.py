import pandas as pd
import joblib

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


print("Loading dataset...")

data = pd.read_csv("ai_module/dataset/crime_dataset_india.csv")


# ------------------------------------------------
# Select useful columns
# ------------------------------------------------

data = data[
    [
        "City",
        "Time of Occurrence",
        "Crime Description",
        "Victim Age",
        "Victim Gender",
        "Weapon Used",
        "Crime Domain"
    ]
]


# ------------------------------------------------
# Clean dataset
# ------------------------------------------------

print("Cleaning dataset...")

data = data.dropna()

data["Victim Age"] = pd.to_numeric(data["Victim Age"], errors="coerce")

data = data.dropna()


# ------------------------------------------------
# Convert Time to Hour
# ------------------------------------------------

data["Time of Occurrence"] = pd.to_datetime(
    data["Time of Occurrence"],
    errors="coerce"
)

data["Hour"] = data["Time of Occurrence"].dt.hour

data = data.drop(columns=["Time of Occurrence"])


# ------------------------------------------------
# Create crime frequency
# ------------------------------------------------

crime_counts = data["City"].value_counts()

data["crime_count"] = data["City"].map(crime_counts)


# ------------------------------------------------
# Create risk label
# ------------------------------------------------

def calculate_risk(x):

    if x > 300:
        return "High"

    elif x > 150:
        return "Medium"

    else:
        return "Low"


data["risk"] = data["crime_count"].apply(calculate_risk)


# ------------------------------------------------
# Encode categorical data
# ------------------------------------------------

print("Encoding features...")

le_city = LabelEncoder()
le_crime = LabelEncoder()
le_gender = LabelEncoder()
le_weapon = LabelEncoder()
le_domain = LabelEncoder()
le_risk = LabelEncoder()


data["City"] = le_city.fit_transform(data["City"])

data["Crime Description"] = le_crime.fit_transform(data["Crime Description"])

data["Victim Gender"] = le_gender.fit_transform(data["Victim Gender"])

data["Weapon Used"] = le_weapon.fit_transform(data["Weapon Used"])

data["Crime Domain"] = le_domain.fit_transform(data["Crime Domain"])

data["risk"] = le_risk.fit_transform(data["risk"])


# ------------------------------------------------
# Training data
# ------------------------------------------------

X = data[
    [
        "City",
        "Hour",
        "Crime Description",
        "Victim Age",
        "Victim Gender",
        "Weapon Used",
        "Crime Domain",
        "crime_count"
    ]
]

y = data["risk"]


# ------------------------------------------------
# Train test split
# ------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# ------------------------------------------------
# Train model
# ------------------------------------------------

print("Training model...")

model = RandomForestClassifier(
    n_estimators=120,
    random_state=42
)

model.fit(X_train, y_train)


# ------------------------------------------------
# Evaluate model
# ------------------------------------------------

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("Model Accuracy:", accuracy)


# ------------------------------------------------
# Save model
# ------------------------------------------------

print("Saving trained model...")

joblib.dump(model, "ai_module/risk_model.pkl")

joblib.dump(le_city, "ai_module/encoder_city.pkl")

joblib.dump(le_crime, "ai_module/encoder_crime.pkl")

joblib.dump(le_gender, "ai_module/encoder_gender.pkl")

joblib.dump(le_weapon, "ai_module/encoder_weapon.pkl")

joblib.dump(le_domain, "ai_module/encoder_domain.pkl")

joblib.dump(le_risk, "ai_module/encoder_risk.pkl")


print("AI model training completed successfully.")