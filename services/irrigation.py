from dataclasses import dataclass

@dataclass
class IrrigationPlan:
    crop: str
    water_liters_per_day: int
    frequency: str
    notes: str


def plan_irrigation(crop: str, stage: str, soil_type: str, weather_rain_chance: str) -> IrrigationPlan:
    base_need = {
        "paddy": 50,
        "banana": 40,
        "coconut": 30,
        "pepper": 20
    }
    per_sq_m = base_need.get(crop.lower(), 30)

    if stage == "seedling":
        per_sq_m *= 0.7
    elif stage == "flowering":
        per_sq_m *= 1.2

    if soil_type == "sandy":
        per_sq_m *= 1.2
    elif soil_type == "clay":
        per_sq_m *= 0.8

    if weather_rain_chance == "high":
        per_sq_m *= 0.5

    total_liters = int(per_sq_m * 100)

    frequency = "Daily" if weather_rain_chance == "low" else "On non-rainy days"

    notes = "Use mulching to reduce evaporation and schedule irrigation early morning or late evening."

    return IrrigationPlan(
        crop=crop,
        water_liters_per_day=total_liters,
        frequency=frequency,
        notes=notes
)
