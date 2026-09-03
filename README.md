# 🛡️ SafeGuard AI - Smart Tourist Safety Monitoring & Crime Risk Prediction System

🌐 **Live Web Application**: [SafeGuard AI - Smart Tourist Safety System](https://tourist-safety-system-rugp.onrender.com/)

**SafeGuard AI** is an advanced, AI-powered web platform built to protect tourists, predict regional crime risks, provide 1-click emergency SOS alerts, locate nearby police stations, and offer an interactive All-India Monuments Heritage Portal with AI Audio Voice Guides.

---

## 🌟 Key Features & Capabilities

### 🌐 1. Live Deployment & Protection (`https://tourist-safety-system-rugp.onrender.com/`)
- Deployed live on Render cloud infrastructure with automatic SSL HTTPS security, database migrations, and static asset delivery via WhiteNoise.

### 🚨 2. Emergency SOS & Rapid Telematics (`/sos/`)
- **1-Click Mobile Speed-Dial Helplines**: Instant one-tap calling for `112` (National Emergency), `100` (Police Control), `108` (Ambulance), and `1091` (Women Safety).
- **GPS SOS Broadcast**: Transmits live latitude and longitude coordinates directly to authority dispatchers.

### 🏛️ 3. All-India Monuments & Heritage Portal (`/tourist-spots/`)
- **Comprehensive Monument Database**: Detailed records for historical heritage sites across Indian states (*Sanchi Stupa, Bhimbetka Rock Shelters, Khajuraho Temples, Gwalior Fort, Orchha Fort, Sawalmendha Satpura Reserve, Ajanta Caves, Ellora Kailash Temple, Gateway of India, Raigad Fort, Amer Fort, Taj Mahal, Qutub Minar, Rani ki Vav*).
- **Authentic Monument Photography**: High-definition verified Wikipedia & Wikimedia Commons photography matching each exact monument.
- **Search & Filtering**: Search box, state dropdown filter, and category quick-filter chips (*UNESCO Heritage, Ancient Caves, Forts & Castles, Palaces, Nature Reserves*).

### 🔊 4. Dedicated Monument Showcase & AI Audio Tour Guide (`/tourist-spot/<spot_id>/`)
- **Hero Image & Deep History**: Full-page showcase with extensive historical chronicles, founding emperors/dynasties, architectural techniques, visitor guidelines, and emergency police response bar.
- **AI Audio Voice Tour Guide**: Powered by Web Speech Synthesis (`window.speechSynthesis`) with **Play**, **Pause**, and **Stop** narration controls.

### 🤖 5. Floating AI Tourist Safety Assistant (`/ai-chat/`)
- Glassmorphic floating AI chatbot widget accessible on all pages.
- Provides real-time automated safety advice for police lookups, emergency SOS guidance, medical assistance, late-night travel safety, and women safety helplines.

### 🚔 6. Nearest Police Station Lookup (`/nearest-police/`)
- **Proximity Bias Engine**: Uses Geoapify Places API v2 + OpenStreetMap Nominatim geocoding proxy to find nearest police stations within 50km.
- **Interactive Map**: Live GPS detection, search box fallback, draggable pin, real-time distance calculation badges, and 1-click Google Maps directions.

### 📊 7. Authority Command Center Dashboard (`/dashboard/`)
- **Web Audio API Siren Alert**: Automatic audio siren synthesizer alerts dispatchers whenever an active emergency SOS alert is received.
- **10-Second Telemetry Refresh**: Continuous background data polling.

### 🎨 8. Modern Glassmorphic Design System & Dynamic Theme Switcher
- Styled in dark glassmorphism (`#090d16` background with frosted glass cards).
- **5 Real-Time UI Themes** with automatic `localStorage` persistence:
  1. 🌌 **Midnight Cyber (Default)**
  2. 🟧 **Neon Orange**
  3. 💎 **Sapphire Ocean**
  4. 🌿 **Emerald Forest**
  5. ☀️ **Clean Light**

---

## 🛠️ Technology Stack

- **Backend Framework:** Django (Python 3.14)
- **Machine Learning:** `scikit-learn` (`RandomForestClassifier` trained on Indian crime dataset)
- **Database:** Microsoft SQL Server (`mssql-django` + `pyodbc`) / SQLite fallback
- **Geospatial APIs:** Geoapify Places API v2, Nominatim OpenStreetMap API
- **Frontend Design:** HTML5, CSS3 Glassmorphism, JavaScript ES6+, FontAwesome 6, Leaflet.js
- **Audio & Speech:** Web Speech API (`SpeechSynthesisUtterance`), Web Audio API (`AudioContext` Siren Oscillator)
- **Deployment & Hosting:** Render Cloud (`https://tourist-safety-system-rugp.onrender.com/`), Gunicorn, WhiteNoise

---

## 📁 Project Architecture

```text
Tourist_safety_system/
├── manage.py                   # Django management script
├── requirements.txt             # Python packages
├── Procfile                    # Deployment configuration
├── render.yaml                 # Render cloud blueprint configuration
├── .env                        # Private API keys & secret keys (Git Ignored)
├── .env.example                # Template for environment configuration
├── config/                     # Django core settings & root URLs
│   ├── settings.py
│   └── urls.py
├── apps/
│   ├── users/                  # Tourist registration & home landing
│   ├── incidents/              # Incident reporting system
│   └── monitoring/             # Core safety, SOS, police, spots & dashboard
│       ├── tourist_spots_data.py
│       ├── views.py
│       ├── urls.py
│       └── models.py
├── ai_module/                  # AI Machine Learning pipeline
│   ├── train_model.py          # Model training script
│   ├── risk_prediction.py      # ML inference helper
│   ├── risk_model.pkl          # Trained RandomForest classifier
│   └── encoders/*.pkl          # Feature encoders
├── templates/                  # Glassmorphic HTML5 templates
├── static/                     # CSS & JS assets
    ├── style.css
    └── scripts.js
```

---

## 🚀 Setup & Installation Guide

### 1) Clone Repository & Install Dependencies
```bash
git clone https://github.com/utk712/Tourist-Safety-System.git
cd Tourist-Safety-System
pip install -r requirements.txt
```

### 2) Environment Configuration (`.env`)
Create a `.env` file in the project root:
```env
GEOAPIFY_API_KEY=your_geoapify_api_key_here
SECRET_KEY=your_django_secret_key
DEBUG=True
```

### 3) Train AI Model (Optional)
```bash
python ai_module/train_model.py
```

### 4) Database Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5) Launch Server
```bash
python manage.py runserver
```

Open your browser at **`http://127.0.0.1:8000/`** or visit the live deployment at **`https://tourist-safety-system-rugp.onrender.com/`**.

---

## 🔒 Security & Privacy

- Sensitive API keys (`GEOAPIFY_API_KEY`, `SECRET_KEY`) are protected inside `.env` and listed in `.gitignore` so they are **never exposed or committed to public Git repositories**.

---

## 📄 License

Developed for Smart Tourist Safety & Protection Systems. Licensed under MIT.
