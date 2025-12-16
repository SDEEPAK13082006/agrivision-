from dataclasses import dataclass

@dataclass
class WeatherAlert:
    type: str
    level: str
    message: str


def get_mock_weather_and_risk(district: str, crop: str) -> list[WeatherAlert]:
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
