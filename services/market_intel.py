from dataclasses import dataclass
from typing import List

@dataclass
class MarketPrice:
    market: str
    crop: str
    price_rs_per_kg: float
    distance_km: int


MOCK_PRICES = [
    {"market": "Alappuzha Mandi", "crop": "Paddy", "price": 25, "distance": 10},
    {"market": "Kottayam Market", "crop": "Paddy", "price": 24, "distance": 30},
    {"market": "Trivandrum Market", "crop": "Banana", "price": 40, "distance": 15},
    {"market": "Kollam Market", "crop": "Banana", "price": 38, "distance": 25},
]


def get_best_market(crop: str, district: str) -> List[MarketPrice]:
    results: List[MarketPrice] = []
    for row in MOCK_PRICES:
        if row["crop"].lower() == crop.lower():
            results.append(
                MarketPrice(
                    market=row["market"],
                    crop=row["crop"],
                    price_rs_per_kg=row["price"],
                    distance_km=row["distance"]
                )
            )
    results.sort(key=lambda x: x.price_rs_per_kg, reverse=True)
    return results
