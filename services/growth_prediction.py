from dataclasses import dataclass


@dataclass
class PlantPrediction:
    crop: str
    land_size_acres: float
    expected_yield_tons: float
    days_to_harvest: int
    expected_profit_rs: int
    notes: str


# Simple reference data for a few common Kerala crops.
# Values are approximate and for CCP demo purposes only.
CROP_GROWTH_DB = {
    "paddy": {
        "yield_t_per_acre": 1.2,  # tonnes per acre
        "days_to_harvest": 120,
        "price_rs_per_ton": 20000,
        "notes": "Normal duration paddy variety under good management."
    },
    "banana": {
        "yield_t_per_acre": 8.0,
        "days_to_harvest": 300,
        "price_rs_per_ton": 35000,
        "notes": "Nendran/robusta type banana with proper fertilizer and irrigation."
    },
    "coconut": {
        "yield_t_per_acre": 1.0,
        "days_to_harvest": 365,
        "price_rs_per_ton": 30000,
        "notes": "Bearing coconut garden (not newly planted). Estimate is for one year."
    },
    "pepper": {
        "yield_t_per_acre": 0.4,
        "days_to_harvest": 240,
        "price_rs_per_ton": 500000,
        "notes": "Mature black pepper vines under average management."
    },
}


def predict_growth(crop: str, land_size_acres: float) -> PlantPrediction:
    """Return a rough plant growth and profit prediction for a crop.

    This is a simple rule-based approximation meant for demonstration only.
    """
    key = crop.strip().lower()
    info = CROP_GROWTH_DB.get(key)

    # If crop not in our table, fall back to a generic assumption.
    if not info:
        # Generic: moderate yield and price
        yield_t_per_acre = 2.0
        days_to_harvest = 150
        price_rs_per_ton = 25000
        notes = "Generic estimate used (crop not in database)."
    else:
        yield_t_per_acre = info["yield_t_per_acre"]
        days_to_harvest = info["days_to_harvest"]
        price_rs_per_ton = info["price_rs_per_ton"]
        notes = info["notes"]

    total_yield = round(yield_t_per_acre * land_size_acres, 2)
    expected_profit = int(total_yield * price_rs_per_ton)

    return PlantPrediction(
        crop=crop,
        land_size_acres=land_size_acres,
        expected_yield_tons=total_yield,
        days_to_harvest=days_to_harvest,
        expected_profit_rs=expected_profit,
        notes=notes,
    )
