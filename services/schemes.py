from dataclasses import dataclass
from typing import List

@dataclass
class Scheme:
    name: str
    department: str
    description: str
    eligibility: str
    how_to_apply: str


SCHEMES = [
    Scheme(
        name="PM-KISAN",
        department="Central Government",
        description="Income support of ₹ 6,000/year to small and marginal farmers.",
        eligibility="Owner cultivator with up to 2 ha land.",
        how_to_apply="Register via Krishi Bhavan or online PM-KISAN portal."
    ),
    Scheme(
        name="Karshaka Insurance Scheme",
        department="Government of Kerala",
        description="Insurance coverage for crop loss due to natural calamities.",
        eligibility="Registered farmers under state agriculture department.",
        how_to_apply="Apply through local Krishi Bhavan / agriculture officer."
    ),
]


def get_schemes_for_farmer(land_size_acres: float, is_small_farmer: bool) -> List[Scheme]:
    results = []
    for s in SCHEMES:
        if "PM-KISAN" in s.name and land_size_acres <= 5:
            results.append(s)
        elif "Insurance" in s.name:
            results.append(s)
    return results
