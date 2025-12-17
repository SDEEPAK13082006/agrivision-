from dataclasses import dataclass
from typing import List, Dict

@dataclass
class CropSuggestion:
    name: str
    season: str
    expected_yield_t_per_ha: float
    expected_profit_rs_per_ha: int
    reasoning: str

# All 14 districts of Kerala
KERALA_DISTRICTS = [
    "thiruvananthapuram", "kollam", "pathanamthitta", "alappuzha",
    "kottayam", "idukki", "ernakulam", "thrissur", "palakkad",
    "malappuram", "kozhikode", "wayanad", "kannur", "kasaragod"
]

CROPS_DB = [
    {
        "name": "Paddy",
        "soil": ["clay", "loam"],
        "districts": ["Alappuzha", "Kottayam", "Thrissur", "Palakkad"],
        "season": "Kharif (Jun–Oct)",
        "water_need": "high",
        "yield_t_per_ha": 3.0,
        "profit_rs_per_ha": 50000
    },
    {
        "name": "Banana",
        "soil": ["loam", "laterite"],
        "districts": ["Thiruvananthapuram", "Kollam", "Kozhikode", "Kannur"],
        "season": "Year-round (best Jun–Aug planting)",
        "water_need": "medium",
        "yield_t_per_ha": 20.0,
        "profit_rs_per_ha": 120000
    },
    {
        "name": "Coconut",
        "soil": ["laterite", "sandy"],
        "districts": ["All"],
        "season": "Perennial",
        "water_need": "medium",
        "yield_t_per_ha": 5.0,
        "profit_rs_per_ha": 80000
    },
    {
        "name": "Pepper",
        "soil": ["loam", "laterite"],
        "districts": ["Idukki", "Wayanad", "Kottayam"],
        "season": "Perennial (cool, humid)",
        "water_need": "medium",
        "yield_t_per_ha": 1.5,
        "profit_rs_per_ha": 150000
    }
]


def recommend_crops(
    soil_type: str,
    land_size_acres: float,
    district: str,
    season: str
) -> List[CropSuggestion]:
    # Check if district is in Kerala
    if district.lower().strip() not in KERALA_DISTRICTS:
        return []  # Return empty list for non-Kerala districts

    matches: List[Dict] = []

    for crop in CROPS_DB:
        score = 0

        if soil_type.lower() in [s.lower() for s in crop["soil"]]:
            score += 2

        if "all" in [d.lower() for d in crop["districts"]] or \
           district.lower() in [d.lower() for d in crop["districts"]]:
            score += 2

        if season.lower() in crop["season"].lower():
            score += 1

        if land_size_acres <= 2 and crop["profit_rs_per_ha"] > 100000:
            score += 1

        if score > 0:
            matches.append({"score": score, "crop": crop})

    matches.sort(key=lambda x: x["score"], reverse=True)
    top = matches[:3]

    suggestions: List[CropSuggestion] = []
    for item in top:
        c = item["crop"]
        factor = land_size_acres / 2.47  # acres to hectares
        suggestions.append(
            CropSuggestion(
                name=c["name"],
                season=c["season"],
                expected_yield_t_per_ha=c["yield_t_per_ha"] * factor,
                expected_profit_rs_per_ha=int(c["profit_rs_per_ha"] * factor),
                reasoning=f"Matched soil ({soil_type}), district ({district}) and season ({season})."
            )
        )
    return suggestions
