# AI-Powered Personal Farming Assistant for Kerala Farmers

This is a CCP project implementation of an **AI-powered personal farming assistant** for Kerala farmers.
It is built as a simple **Flask web application** with rule-based logic and mock data.

## Features

1. **Personalized Crop Advisor** – Suggests suitable crops based on soil type, land size, district and season.
2. **Weather & Risk Alerts** – Simple, district-based mock alerts with disease risk hints.
3. **Pest & Disease Assistant** – Text-based symptom input and rule-based suggestions with organic options.
4. **Soil Health & Fertilizer Planner** – NPK dose calculator with organic fertilizer guidance.
5. **Market Price Intelligence** – Mock nearby market prices and best-rate suggestion.
6. **Water & Irrigation Scheduler** – Simple water requirement estimation and frequency.
7. **Government Schemes & Insurance Guide** – Basic list of relevant schemes and how to apply.
8. **Bilingual UI (English + Malayalam labels)** – Farmer-friendly navigation.

## How to Run

1. Install Python 3.
2. Open PowerShell in the `farming-assistant` folder.
3. Create and activate a virtual environment, install dependencies, and run the app:

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

4. Open the printed URL (usually `http://127.0.0.1:5000/`) in your browser.

## Mapping to SIH25074 Blueprint

- **Crop Advisor** → `/crop-advisor` route and `services/crop_advisor.py`.
- **Weather & Risk** → `/weather` and `services/weather_risk.py`.
- **Pest & Disease** → `/pest` and `services/pest_diagnosis.py`.
- **Soil & Fertilizer** → `/soil` and `services/soil_fertilizer.py`.
- **Market Intelligence** → `/market` and `services/market_intel.py`.
- **Irrigation Scheduler** → `/irrigation` and `services/irrigation.py`.
- **Schemes & Insurance Guide** → `/schemes` and `services/schemes.py`.

The AI logic is implemented as **transparent rule-based decision making** that can be
explained easily in a CCP viva (no heavy ML required). Future work can include:

- Real-time weather API integration (OpenWeatherMap).
- Image-based pest detection using a trained CNN model.
- Voice input/output in Malayalam using Web Speech API or cloud speech services.
- Integration with live market price APIs.
