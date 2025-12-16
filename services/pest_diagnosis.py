from dataclasses import dataclass
from typing import List, Dict


@dataclass
class PestDiagnosis:
    crop: str
    likely_disease: str
    confidence: int
    treatment: str
    organic_option: str
    caution: str


# Very small rule-based database for common Kerala crop diseases.
_DISEASE_DB: List[Dict] = [
    {
        "crop": "paddy",
        "name": "Blast (leaf blast)",
        "keywords": ["brown spot", "diamond", "lesion", "blast"],
        "treatment": "Use blast-tolerant varieties, avoid excess nitrogen; spray recommended fungicide as per agri officer.",
        "organic": "Apply neem cake and maintain proper spacing for good air movement.",
        "caution": "Do not spray fungicides repeatedly without guidance; follow label dose only.",
    },
    {
        "crop": "paddy",
        "name": "Bacterial leaf blight",
        "keywords": ["leaf tip", "drying", "kresek", "yellowing from tip"],
        "treatment": "Drain excess water, apply balanced fertilizers; use copper-based bactericides if advised by agri officer.",
        "organic": "Use seed treatment with beneficial microbes and avoid injuring plants during weeding.",
        "caution": "Do not overuse copper; follow recommended intervals and safety measures.",
    },
    {
        "crop": "banana",
        "name": "Panama wilt (Fusarium wilt)",
        "keywords": ["yellowing", "yellow leaf", "wilt", "v-shape"],
        "treatment": "Remove and destroy heavily infected plants; improve drainage and use disease-free suckers.",
        "organic": "Apply Trichoderma-enriched compost around the plant base and avoid waterlogging.",
        "caution": "Do not replant banana in the same pit immediately; follow crop rotation.",
    },
    {
        "crop": "banana",
        "name": "Sigatoka leaf spot",
        "keywords": ["yellow streak", "leaf spot", "brown spot", "strip"],
        "treatment": "Remove severely affected leaves and spray recommended fungicide in dry weather.",
        "organic": "Use neem oil or botanical extracts as preventive sprays and keep field well aerated.",
        "caution": "Always use clean tools when removing leaves to avoid spreading disease.",
    },
    {
        "crop": "coconut",
        "name": "Bud rot",
        "keywords": ["bud rot", "crown", "spear leaf", "rotting"],
        "treatment": "Remove and destroy affected tissues; apply recommended fungicide on the crown as per agri officer.",
        "organic": "Improve drainage around the palm and avoid water stagnation near the trunk.",
        "caution": "Work carefully at the crown; use safety equipment and avoid climbing in wet conditions.",
    },
    {
        "crop": "pepper",
        "name": "Quick wilt (Phytophthora)",
        "keywords": ["sudden wilt", "blackening", "base", "root rot"],
        "treatment": "Improve drainage, apply recommended fungicide drench around the vine base.",
        "organic": "Apply Trichoderma-enriched compost and mulch; avoid waterlogging.",
        "caution": "Monitor neighbouring vines regularly; early detection reduces spread.",
    },
]


def diagnose_pest_mock(crop: str, symptom_text: str) -> PestDiagnosis:
    """Simple rule-based diagnosis using crop + text symptoms.

    This is a demo helper and not a replacement for expert field visit.
    """

    text = (symptom_text or "").lower()
    ckey = crop.strip().lower()

    best_match = None
    best_score = 0

    for entry in _DISEASE_DB:
        if entry["crop"] != ckey:
            continue
        score = 0
        for kw in entry["keywords"]:
            if kw in text:
                score += 1
        if score > best_score:
            best_score = score
            best_match = entry

    if best_match and best_score > 0:
        confidence = 60 + best_score * 10
        return PestDiagnosis(
            crop=crop,
            likely_disease=best_match["name"],
            confidence=min(confidence, 95),
            treatment=best_match["treatment"],
            organic_option=best_match["organic"],
            caution=best_match["caution"],
        )

    # Fallback when we cannot clearly match symptoms
    return PestDiagnosis(
        crop=crop,
        likely_disease="Not clearly identified",
        confidence=50,
        treatment="Consult local Krishi Bhavan or an agriculture officer with clear photos for proper diagnosis.",
        organic_option="Use neem oil spray (2-3 ml/litre) as a general preventive measure and improve field hygiene.",
        caution="Avoid random pesticide mixing. Always follow recommended dose and safety instructions.",
    )
