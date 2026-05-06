# Smart Tourist Safety Monitoring System

A Django-based web platform that helps monitor tourist safety, raise SOS alerts, report incidents, and predict crime risk using a trained ML model.

---

## Features

- **Tourist registration**
- **SOS emergency alerts** (stores user + GPS coordinates)
- **Incident reporting**
- **Authority dashboard** (lists tourists, incidents, SOS alerts)
- **Crime risk prediction** (AI model)
- **Crime heatmap & map view** (Leaflet + server-provided predicted points)
- **Nearest police lookup** (Geoapify places API)
- **Live tracking UI** (page + endpoint scaffolding)

---

## Tech Stack

- **Backend:** Django (Python)
- **Database:** Microsoft SQL Server (via `mssql-django` + `pyodbc`)
- **ML:** scikit-learn (`RandomForestClassifier`)
- **Frontend:** Bootstrap 5
- **Maps:** Leaflet + Leaflet.heat

---

## Project Structure

```
Tourist_safety_system/
├─ manage.py
├─ config/
│  ├─ settings.py
│  ├─ urls.py
├─ apps/
│  ├─ users/
│  │  ├─ models.py
│  │  ├─ views.py
│  │  └─ urls.py
│  ├─ incidents/
│  │  ├─ models.py
│  │  ├─ views.py
│  │  └─ urls.py
│  └─ monitoring/
│     ├─ models.py
│     ├─ views.py
│     └─ urls.py
├─ ai_module/
│  ├─ train_model.py
│  ├─ risk_prediction.py
│  ├─ city_coordinates.py
│  ├─ encoders/*.pkl
│  ├─ risk_model.pkl
│  └─ dataset/crime_dataset_india.csv
├─ templates/
│  └─ *.html
├─ static/
│  └─ *.css, *.js
└─ requirements.txt
```

---

## AI / ML Model

- **Dataset:** `ai_module/dataset/crime_dataset_india.csv`
- **Training:** `ai_module/train_model.py`
- **Inference helper:** `ai_module/risk_prediction.py`
  - Loads:
    - `ai_module/risk_model.pkl`
    - encoders: `encoder_city.pkl`, `encoder_crime.pkl`, `encoder_gender.pkl`, `encoder_weapon.pkl`, `encoder_domain.pkl`, `encoder_risk.pkl`
  - Main function:
    - `predict_risk(city, hour, crime_description, victim_age, victim_gender, weapon_used, crime_domain, crime_count)`

> Note: `predict_risk` uses a safe transform for unknown categorical values.

---

## Routes / URLs

### App routes

From `apps/users/urls.py`:
- `GET /` → `apps.users.views.home` → `templates/home.html`
- `POST /register/` → `apps.users.views.register_tourist` → redirects to `/`

From `apps/incidents/urls.py`:
- `POST /incidents/` → `apps.incidents.views.report_incident` → `templates/incidents_success.html`

From `apps/monitoring/urls.py`:
- `POST /sos/` → `sos_alert` → `templates/sos_success.html`
- `GET /dashboard/` → `dashboard` → `templates/dashboard.html`
- `GET /risk-check/` → `check_location_risk` → returns JSON
- `GET /crime-heatmap/` → `crime_heatmap_data` → returns JSON array
- `GET /crime-map/` → `crime_map` → `templates/map_dashboard.html`

Pages:
- `GET /live-risk/` → `templates/live_risk.html`
- `GET /live-tracking/` → `templates/live_tracking.html`
- `GET /sos-map/` → `templates/sos_dashboard.html`
- `GET /nearest-police/` → `templates/nearest_police.html`

APIs:
- `GET /sos-data/` → SOS coordinates list (JSON)
- `POST /update-location/` → location received response
- `GET /nearest-police-data/` → nearest police stations via Geoapify

---

## Setup & Run

### 1) Install dependencies

```bash
pip install -r reqirements.txt
```

### 2) Configure SQL Server

Edit `config/settings.py`:
- `DATABASES['default']` must match your SQL Server instance.
- Current configuration uses:
  - `driver`: `ODBC Driver 17 for SQL Server`
  - `trusted_connection`: `yes`

### 3) Migrate database

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4) (Optional) Train the ML model

If you need to retrain:

```bash
python ai_module/train_model.py
```

Ensure `ai_module/risk_model.pkl` and encoder `.pkl` files exist after training.

### 5) Run the server

```bash
python manage.py runserver
```

Open:
- `http://127.0.0.1:8000/`

---

## Example API Usage

### Risk check

```text
GET /risk-check/?city=Mumbai&hour=22
```

Response:
```json
{
  "city": "Mumbai",
  "risk_level": "High"
}
```

### Crime heatmap data

```text
GET /crime-heatmap/
```

Response (example):
```json
[
  {"lat": 19.076, "lng": 72.8777, "risk": "High"}
]
```

---

## Security / Notes

- `config/settings.py` currently has `DEBUG = True` and `ALLOWED_HOSTS = ["*"]`.
- `apps/monitoring/views.py` includes a **Geoapify API key** in `get_nearest_police`. For production, move it to environment variables (e.g., `.env`) and do not commit it.

---

## License

Add your license information here (or remove this section). 

