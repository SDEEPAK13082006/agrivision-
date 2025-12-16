from dataclasses import dataclass

@dataclass
class FertilizerPlan:
    crop: str
    nitrogen_kg: float
    phosphorus_kg: float
    potassium_kg: float
    organic_alternative: str
    tips: str


def calculate_fertilizer(crop: str, soil_organic_matter: str, land_size_acres: float) -> FertilizerPlan:
    base_npk = {
        "paddy":  (40, 20, 20),
        "banana": (80, 40, 60),
        "coconut": (30, 15, 40),
        "pepper": (50, 25, 25)
    }
    ckey = crop.lower()
    n, p, k = base_npk.get(ckey, (40, 20, 20))

    factor = land_size_acres
    n *= factor
    p *= factor
    k *= factor

    if soil_organic_matter == "high":
        n *= 0.7
        p *= 0.8
        k *= 0.8
        tips = "Soil organic matter is high. Reduce chemical fertilizer and prefer organic manures."
    elif soil_organic_matter == "low":
        tips = "Organic matter is low. Add FYM/compost and green manure crops."
    else:
        tips = "Maintain balanced use of chemical fertilizers and organic manures."

    organic_alt = "Apply 5–10 tons/acre of well-decomposed FYM or compost."

    return FertilizerPlan(
        crop=crop,
        nitrogen_kg=round(n, 1),
        phosphorus_kg=round(p, 1),
        potassium_kg=round(k, 1),
        organic_alternative=organic_alt,
        tips=tips
)
