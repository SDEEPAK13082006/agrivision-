from dataclasses import dataclass

@dataclass
class WeatherAlert:
    type: str
    level: str
    message: str

# All 14 districts of Kerala
KERALA_DISTRICTS = [
    "thiruvananthapuram", "kollam", "pathanamthitta", "alappuzha",
    "kottayam", "idukki", "ernakulam", "thrissur", "palakkad",
    "malappuram", "kozhikode", "wayanad", "kannur", "kasaragod"
]


def get_mock_weather_and_risk(district: str, crop: str) -> list[WeatherAlert]:
    # Check if district is in Kerala
    if district.lower().strip() not in KERALA_DISTRICTS:
        return []  # Return empty list for non-Kerala districts

    alerts = []

    if district.lower() in ["idukki", "wayanad"]:
        alerts.append(WeatherAlert(
            type="rain",
            level="high",
            message="Heavy rainfall expected in the next 3 days. Avoid waterlogging in fields."
        ))
        if crop.lower() in ["pepper", "cardamom", "banana"]:
            alerts.append(WeatherAlert(
                type="disease-risk",
                level="medium",
                message="High humidity may trigger fungal diseases. Monitor leaves for spots."
            ))
    else:
        alerts.append(WeatherAlert(
            type="rain",
            level="medium",
            message="Moderate showers likely. Plan irrigation accordingly."
        ))

    return alerts
