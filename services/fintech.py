"""
Agri-FinTech Services for Kerala Farmers
Real-world data based on Kerala Government and Central Government schemes.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional

# ============================================================================
# KERALA AGRICULTURAL LOAN SCHEMES (Real Data)
# Sources: Kerala State Co-operative Bank, NABARD, RBI guidelines
# ============================================================================

KERALA_AGRI_LOANS = [
    {
        "id": "kcc",
        "name": "Kisan Credit Card (KCC)",
        "provider": "All Scheduled Banks / Kerala Co-operative Banks",
        "max_amount": 300000,  # ₹3 lakh limit for interest subvention
        "interest_rate": 4.0,  # After 3% interest subvention
        "original_rate": 7.0,
        "tenure_months": 12,
        "collateral_required": False,  # Up to ₹1.6 lakh
        "collateral_limit": 160000,
        "eligible_crops": ["Paddy", "Banana", "Coconut", "Pepper", "Rubber", "Vegetables", "Tapioca"],
        "min_land_acres": 0.5,
        "description": "Short-term crop loan with 3% interest subvention from Government of India. Additional 3% subvention for prompt repayment.",
        "documents": ["Land documents / Pattayam", "Aadhaar Card", "Bank passbook", "Passport photo"],
        "apply_at": "Any bank branch or Kerala Co-operative Bank"
    },
    {
        "id": "kscardb_mtl",
        "name": "Medium Term Agricultural Loan",
        "provider": "Kerala State Co-operative Agricultural & Rural Development Bank (KSCARDB)",
        "max_amount": 1000000,  # Up to ₹10 lakh
        "interest_rate": 9.5,
        "original_rate": 9.5,
        "tenure_months": 60,  # 5 years
        "collateral_required": True,
        "collateral_limit": 0,
        "eligible_crops": ["Coconut", "Rubber", "Pepper", "Cardamom", "Coffee", "Arecanut"],
        "min_land_acres": 1.0,
        "description": "Medium-term loan for plantation crops, farm development, land improvement, and agricultural infrastructure.",
        "documents": ["Land documents with encumbrance certificate", "Aadhaar & PAN", "Income certificate", "Agricultural officer recommendation"],
        "apply_at": "KSCARDB branches across Kerala"
    },
    {
        "id": "kerala_bank_agri",
        "name": "Kerala Bank Agricultural Loan",
        "provider": "Kerala State Co-operative Bank (Kerala Bank)",
        "max_amount": 500000,
        "interest_rate": 7.0,
        "original_rate": 7.0,
        "tenure_months": 36,
        "collateral_required": False,
        "collateral_limit": 100000,
        "eligible_crops": ["All crops"],
        "min_land_acres": 0.25,
        "description": "General agricultural loan for small and marginal farmers in Kerala for crop production and allied activities.",
        "documents": ["Land ownership proof", "Aadhaar Card", "Ration card", "Bank statement"],
        "apply_at": "Kerala Bank / Primary Agricultural Co-operative Societies (PACS)"
    },
    {
        "id": "nabard_dairy",
        "name": "Dairy Entrepreneurship Development Scheme",
        "provider": "NABARD through Kerala Banks",
        "max_amount": 700000,
        "interest_rate": 10.5,
        "original_rate": 10.5,
        "tenure_months": 72,  # 6 years
        "collateral_required": True,
        "collateral_limit": 100000,
        "eligible_crops": ["Dairy farming", "Cattle rearing"],
        "min_land_acres": 0.1,
        "description": "Loan for setting up small dairy farms with 2-10 milch animals. 25% back-end capital subsidy available.",
        "documents": ["Project report", "Land documents", "Quotations for animals/equipment", "Training certificate if any"],
        "apply_at": "Any scheduled bank or Regional Rural Bank"
    },
    {
        "id": "agri_gold_loan",
        "name": "Agricultural Gold Loan",
        "provider": "Kerala Bank / Federal Bank / SBI",
        "max_amount": 2500000,  # Up to ₹25 lakh
        "interest_rate": 7.0,
        "original_rate": 7.0,
        "tenure_months": 12,
        "collateral_required": True,  # Gold as collateral
        "collateral_limit": 0,
        "eligible_crops": ["All agricultural purposes"],
        "min_land_acres": 0,
        "description": "Quick loan against gold ornaments for agricultural purposes. Fast disbursement within hours.",
        "documents": ["Gold ornaments", "Aadhaar Card", "Land documents (for agricultural purpose proof)"],
        "apply_at": "Bank branches"
    }
]

# ============================================================================
# KERALA CROP INSURANCE SCHEMES (Real Data)
# Sources: PMFBY, Kerala State Crop Insurance, Agriculture Department
# ============================================================================

KERALA_CROP_INSURANCE = {
    "pmfby": {
        "name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
        "provider": "Agriculture Insurance Company of India (AIC) / Other empanelled insurers",
        "premium_kharif": 2.0,  # 2% of sum insured for Kharif crops
        "premium_rabi": 1.5,  # 1.5% for Rabi crops
        "premium_commercial": 5.0,  # 5% for commercial/horticultural crops
        "coverage": [
            "Yield loss due to natural calamities",
            "Prevented sowing/planting risk",
            "Post-harvest losses (up to 14 days)",
            "Localized calamities (hailstorm, landslide, inundation)"
        ],
        "sum_insured_per_ha": {
            "Paddy": 45000,
            "Banana": 150000,
            "Coconut": 35000,
            "Pepper": 75000,
            "Vegetables": 50000,
            "Tapioca": 35000
        },
        "documents": ["Land records", "Sowing certificate", "Bank account", "Aadhaar"],
        "deadline": "Kharif: July 31, Rabi: December 31"
    },
    "kerala_state": {
        "name": "Kerala State Crop Insurance Scheme",
        "provider": "Kerala Agriculture Department",
        "premium_rate": 2.0,  # Subsidized premium
        "coverage": [
            "Flood damage",
            "Drought damage", 
            "Pest and disease outbreak",
            "Wild animal attack"
        ],
        "max_compensation": {
            "Paddy": 25000,
            "Banana": 50000,
            "Vegetables": 30000,
            "Coconut": 15000,
            "Pepper": 40000
        },
        "documents": ["Krishi Bhavan registration", "Land documents", "Crop details"],
        "apply_at": "Krishi Bhavan"
    },
    "coconut_insurance": {
        "name": "Coconut Palm Insurance Scheme",
        "provider": "Coconut Development Board / AIC",
        "premium_per_palm": 9.0,  # ₹9 per palm (farmer share after subsidy)
        "actual_premium": 14.0,  # ₹14 per palm
        "subsidy": 5.0,  # ₹5 subsidy from CDB
        "sum_insured_per_palm": 1750,
        "coverage": ["Natural calamities", "Pest attack", "Disease"],
        "max_palms": 50,
        "documents": ["Ownership proof", "Palm count certificate from Krishi Bhavan"],
        "apply_at": "Krishi Bhavan or Coconut Development Board"
    }
}

# ============================================================================
# KERALA AGRICULTURAL SUBSIDIES (Real Data)
# Sources: Kerala Agriculture Department, Central Schemes
# ============================================================================

KERALA_SUBSIDIES = [
    {
        "id": "pm_kisan",
        "name": "PM-KISAN Samman Nidhi",
        "amount": 6000,
        "frequency": "Annual (₹2,000 x 3 instalments)",
        "eligibility": {
            "land_max_ha": 2.0,  # Small and marginal farmers
            "income_limit": None,
            "categories": ["All land-owning farmer families"]
        },
        "description": "Direct income support of ₹6,000 per year to all farmer families.",
        "documents": ["Aadhaar", "Land records", "Bank account"],
        "apply_at": "Common Service Centre / Krishi Bhavan / pmkisan.gov.in"
    },
    {
        "id": "drip_irrigation",
        "name": "Micro Irrigation Subsidy (PMKSY)",
        "amount_percent": 55,  # 55% for small farmers
        "amount_percent_marginal": 55,
        "max_amount_per_ha": 100000,
        "eligibility": {
            "land_min_acres": 0.25,
            "crops": ["Vegetables", "Banana", "Coconut", "Pepper", "Fruit crops"]
        },
        "description": "55% subsidy on drip and sprinkler irrigation systems under Pradhan Mantri Krishi Sinchayee Yojana.",
        "documents": ["Land documents", "Quotation from approved supplier", "Bank account"],
        "apply_at": "Krishi Bhavan / eMISSION portal"
    },
    {
        "id": "farm_mechanization",
        "name": "Farm Mechanization Subsidy (SMAM)",
        "amount_percent": 50,  # 50% for general, 60% for SC/ST
        "amount_percent_scst": 60,
        "eligible_equipment": ["Power tiller", "Transplanter", "Harvester", "Sprayer", "Pump sets"],
        "max_amount": 150000,
        "eligibility": {
            "land_min_acres": 0.5
        },
        "description": "50-60% subsidy on farm machinery under Sub-Mission on Agricultural Mechanization.",
        "documents": ["Land documents", "Aadhaar", "Quotation", "SC/ST certificate if applicable"],
        "apply_at": "Krishi Bhavan / agrimachinery.nic.in"
    },
    {
        "id": "organic_farming",
        "name": "Paramparagat Krishi Vikas Yojana (PKVY)",
        "amount_per_ha": 50000,  # Over 3 years
        "coverage_years": 3,
        "eligibility": {
            "land_min_acres": 0.5,
            "cluster_size": 20  # Minimum 20 farmers in a cluster
        },
        "description": "₹50,000/ha over 3 years for organic farming inputs, certification, and marketing.",
        "documents": ["Cluster formation documents", "Land records", "Commitment letter"],
        "apply_at": "Krishi Bhavan / Agriculture Department"
    },
    {
        "id": "seed_subsidy",
        "name": "Certified Seed Subsidy",
        "amount_percent": 50,
        "crops": {
            "Paddy": "₹25/kg subsidy",
            "Vegetables": "50% subsidy",
            "Pulses": "₹100/kg subsidy"
        },
        "eligibility": {
            "land_min_acres": 0.1
        },
        "description": "Subsidy on certified seeds distributed through Krishi Bhavans and KSSDA.",
        "documents": ["Ration card / Aadhaar", "Land documents"],
        "apply_at": "Krishi Bhavan / Kerala State Seed Development Authority"
    },
    {
        "id": "interest_subvention",
        "name": "Interest Subvention on Crop Loans",
        "interest_benefit": 3.0,  # 3% subvention
        "additional_benefit": 3.0,  # Additional 3% for prompt repayment
        "max_loan": 300000,
        "effective_rate": 4.0,  # After all subventions
        "eligibility": {
            "loan_type": "Short-term crop loan",
            "repayment": "Within 1 year"
        },
        "description": "3% interest subvention on crop loans up to ₹3 lakh. Additional 3% for timely repayment, making effective rate 4%.",
        "documents": ["KCC or crop loan account"],
        "apply_at": "Automatic through bank"
    },
    {
        "id": "pm_kusum",
        "name": "PM-KUSUM Solar Pump Subsidy",
        "amount_percent": 60,  # 30% Central + 30% State
        "central_share": 30,
        "state_share": 30,
        "farmer_share": 40,
        "pump_capacity": "Up to 7.5 HP",
        "eligibility": {
            "land_min_acres": 0.5,
            "water_source": ["Borewell", "Open well", "Canal"]
        },
        "description": "60% subsidy (30% Central + 30% State) on standalone solar pumps for irrigation.",
        "documents": ["Land documents", "Water source proof", "Aadhaar", "Electricity bill (if replacing electric pump)"],
        "apply_at": "ANERT / Krishi Bhavan / mnre.gov.in"
    }
]

# ============================================================================
# RISK ASSESSMENT FACTORS
# ============================================================================

KERALA_DISTRICT_RISK = {
    "Thiruvananthapuram": {"flood": "medium", "drought": "low", "pest": "medium"},
    "Kollam": {"flood": "medium", "drought": "low", "pest": "medium"},
    "Pathanamthitta": {"flood": "high", "drought": "low", "pest": "low"},
    "Alappuzha": {"flood": "high", "drought": "low", "pest": "medium"},
    "Kottayam": {"flood": "high", "drought": "low", "pest": "medium"},
    "Idukki": {"flood": "medium", "drought": "low", "pest": "high"},
    "Ernakulam": {"flood": "medium", "drought": "low", "pest": "medium"},
    "Thrissur": {"flood": "medium", "drought": "medium", "pest": "medium"},
    "Palakkad": {"flood": "low", "drought": "high", "pest": "medium"},
    "Malappuram": {"flood": "medium", "drought": "medium", "pest": "medium"},
    "Kozhikode": {"flood": "medium", "drought": "low", "pest": "medium"},
    "Wayanad": {"flood": "high", "drought": "medium", "pest": "high"},
    "Kannur": {"flood": "medium", "drought": "low", "pest": "medium"},
    "Kasaragod": {"flood": "medium", "drought": "medium", "pest": "medium"}
}

CROP_RISK_FACTORS = {
    "Paddy": {"weather_sensitivity": "high", "pest_risk": "high", "market_volatility": "medium"},
    "Banana": {"weather_sensitivity": "high", "pest_risk": "high", "market_volatility": "high"},
    "Coconut": {"weather_sensitivity": "medium", "pest_risk": "medium", "market_volatility": "low"},
    "Pepper": {"weather_sensitivity": "medium", "pest_risk": "high", "market_volatility": "high"},
    "Rubber": {"weather_sensitivity": "low", "pest_risk": "low", "market_volatility": "high"},
    "Vegetables": {"weather_sensitivity": "high", "pest_risk": "high", "market_volatility": "high"},
    "Tapioca": {"weather_sensitivity": "low", "pest_risk": "medium", "market_volatility": "medium"}
}


# ============================================================================
# FINTECH SERVICE FUNCTIONS
# ============================================================================

@dataclass
class LoanEligibility:
    loan_name: str
    provider: str
    eligible: bool
    max_eligible_amount: int
    interest_rate: float
    tenure_months: int
    monthly_emi: int
    total_repayment: int
    documents_required: List[str]
    apply_at: str
    reason: str

@dataclass 
class InsuranceRecommendation:
    scheme_name: str
    provider: str
    premium_amount: int
    sum_insured: int
    coverage: List[str]
    risk_score: str
    recommendation: str
    documents: List[str]

@dataclass
class SubsidyRecommendation:
    scheme_name: str
    potential_benefit: str
    eligibility_status: str
    description: str
    how_to_apply: str
    documents: List[str]


def calculate_emi(principal: int, annual_rate: float, tenure_months: int) -> int:
    """Calculate EMI using standard formula."""
    if annual_rate == 0:
        return principal // tenure_months
    monthly_rate = annual_rate / 12 / 100
    emi = principal * monthly_rate * ((1 + monthly_rate) ** tenure_months) / (((1 + monthly_rate) ** tenure_months) - 1)
    return int(emi)


def check_loan_eligibility(
    land_size_acres: float,
    crop: str,
    district: str,
    annual_income: int,
    existing_loans: int,
    has_collateral: bool,
    loan_amount_needed: int
) -> List[LoanEligibility]:
    """Check eligibility for various Kerala agricultural loans."""
    
    eligible_loans = []
    
    for loan in KERALA_AGRI_LOANS:
        eligible = True
        reason = "You are eligible for this loan."
        max_eligible = min(loan["max_amount"], loan_amount_needed)
        
        # Check land size requirement
        if land_size_acres < loan["min_land_acres"]:
            eligible = False
            reason = f"Minimum {loan['min_land_acres']} acres of land required."
        
        # Check crop eligibility
        if "All crops" not in loan["eligible_crops"] and "All agricultural purposes" not in loan["eligible_crops"]:
            if crop not in loan["eligible_crops"]:
                eligible = False
                reason = f"This loan is not available for {crop} cultivation."
        
        # Check collateral requirement
        if loan["collateral_required"] and not has_collateral:
            if loan_amount_needed > loan["collateral_limit"]:
                eligible = False
                reason = "Collateral required for this loan amount."
        
        # Adjust eligible amount based on income (rough estimate: 4x annual income)
        income_based_limit = annual_income * 4
        if income_based_limit < max_eligible:
            max_eligible = income_based_limit
            reason += f" Amount limited based on income."
        
        # Consider existing loans
        if existing_loans > 0:
            debt_ratio = existing_loans / max(annual_income, 1)
            if debt_ratio > 0.5:
                max_eligible = int(max_eligible * 0.5)
                reason += " Reduced due to existing debt."
        
        emi = calculate_emi(max_eligible, loan["interest_rate"], loan["tenure_months"])
        total_repayment = emi * loan["tenure_months"]
        
        eligible_loans.append(LoanEligibility(
            loan_name=loan["name"],
            provider=loan["provider"],
            eligible=eligible,
            max_eligible_amount=max_eligible if eligible else 0,
            interest_rate=loan["interest_rate"],
            tenure_months=loan["tenure_months"],
            monthly_emi=emi if eligible else 0,
            total_repayment=total_repayment if eligible else 0,
            documents_required=loan["documents"],
            apply_at=loan["apply_at"],
            reason=reason
        ))
    
    # Sort by eligibility and interest rate
    eligible_loans.sort(key=lambda x: (not x.eligible, x.interest_rate))
    
    return eligible_loans


def analyze_crop_insurance_risk(
    crop: str,
    district: str,
    land_size_acres: float,
    season: str
) -> List[InsuranceRecommendation]:
    """Analyze crop insurance options and risk for Kerala farmers."""
    
    recommendations = []
    land_size_ha = land_size_acres * 0.4047  # Convert acres to hectares
    
    # Get district and crop risk
    district_risk = KERALA_DISTRICT_RISK.get(district, {"flood": "medium", "drought": "medium", "pest": "medium"})
    crop_risk = CROP_RISK_FACTORS.get(crop, {"weather_sensitivity": "medium", "pest_risk": "medium", "market_volatility": "medium"})
    
    # Calculate overall risk score
    risk_points = 0
    if district_risk["flood"] == "high": risk_points += 2
    elif district_risk["flood"] == "medium": risk_points += 1
    if district_risk["drought"] == "high": risk_points += 2
    elif district_risk["drought"] == "medium": risk_points += 1
    if crop_risk["weather_sensitivity"] == "high": risk_points += 2
    elif crop_risk["weather_sensitivity"] == "medium": risk_points += 1
    if crop_risk["pest_risk"] == "high": risk_points += 2
    elif crop_risk["pest_risk"] == "medium": risk_points += 1
    
    if risk_points >= 6:
        risk_score = "HIGH RISK"
        recommendation_text = "Strongly recommended to take comprehensive crop insurance."
    elif risk_points >= 3:
        risk_score = "MEDIUM RISK"
        recommendation_text = "Recommended to take crop insurance for protection."
    else:
        risk_score = "LOW RISK"
        recommendation_text = "Optional but advisable to take basic insurance."
    
    # PMFBY Recommendation
    pmfby = KERALA_CROP_INSURANCE["pmfby"]
    sum_insured_per_ha = pmfby["sum_insured_per_ha"].get(crop, 40000)
    total_sum_insured = int(sum_insured_per_ha * land_size_ha)
    
    if season.lower() in ["kharif", "monsoon"]:
        premium_rate = pmfby["premium_kharif"]
    elif season.lower() in ["rabi", "winter"]:
        premium_rate = pmfby["premium_rabi"]
    else:
        premium_rate = pmfby["premium_commercial"]
    
    premium_amount = int(total_sum_insured * premium_rate / 100)
    
    recommendations.append(InsuranceRecommendation(
        scheme_name=pmfby["name"],
        provider=pmfby["provider"],
        premium_amount=premium_amount,
        sum_insured=total_sum_insured,
        coverage=pmfby["coverage"],
        risk_score=risk_score,
        recommendation=recommendation_text,
        documents=pmfby["documents"]
    ))
    
    # Kerala State Scheme
    kerala_scheme = KERALA_CROP_INSURANCE["kerala_state"]
    max_comp = kerala_scheme["max_compensation"].get(crop, 25000)
    state_premium = int(max_comp * kerala_scheme["premium_rate"] / 100)
    
    recommendations.append(InsuranceRecommendation(
        scheme_name=kerala_scheme["name"],
        provider=kerala_scheme["provider"],
        premium_amount=state_premium,
        sum_insured=max_comp,
        coverage=kerala_scheme["coverage"],
        risk_score=risk_score,
        recommendation="Good additional coverage for Kerala-specific risks.",
        documents=kerala_scheme["documents"]
    ))
    
    # Coconut Insurance if applicable
    if crop.lower() == "coconut":
        coconut_scheme = KERALA_CROP_INSURANCE["coconut_insurance"]
        estimated_palms = int(land_size_acres * 70)  # Approx 70 palms per acre
        palms_to_insure = min(estimated_palms, coconut_scheme["max_palms"])
        coconut_premium = int(palms_to_insure * coconut_scheme["premium_per_palm"])
        coconut_sum = palms_to_insure * coconut_scheme["sum_insured_per_palm"]
        
        recommendations.append(InsuranceRecommendation(
            scheme_name=coconut_scheme["name"],
            provider=coconut_scheme["provider"],
            premium_amount=coconut_premium,
            sum_insured=coconut_sum,
            coverage=coconut_scheme["coverage"],
            risk_score=risk_score,
            recommendation=f"Specific coverage for {palms_to_insure} coconut palms.",
            documents=coconut_scheme["documents"]
        ))
    
    return recommendations


def get_subsidy_recommendations(
    land_size_acres: float,
    crop: str,
    district: str,
    farmer_category: str,  # "general", "sc", "st", "woman"
    has_irrigation: bool,
    organic_interest: bool
) -> List[SubsidyRecommendation]:
    """Get eligible subsidy recommendations for Kerala farmers."""
    
    recommendations = []
    land_size_ha = land_size_acres * 0.4047
    
    # PM-KISAN (Universal for small/marginal farmers)
    if land_size_ha <= 2.0:
        recommendations.append(SubsidyRecommendation(
            scheme_name="PM-KISAN Samman Nidhi",
            potential_benefit="₹6,000 per year (₹2,000 x 3 instalments)",
            eligibility_status="ELIGIBLE" if land_size_ha <= 2.0 else "NOT ELIGIBLE",
            description="Direct income support transferred to your bank account every 4 months.",
            how_to_apply="Register at pmkisan.gov.in or visit Krishi Bhavan",
            documents=["Aadhaar Card", "Land records", "Bank passbook"]
        ))
    
    # Micro Irrigation Subsidy
    if crop in ["Vegetables", "Banana", "Coconut", "Pepper", "Arecanut"]:
        subsidy_percent = 55
        max_benefit = int(100000 * land_size_ha * subsidy_percent / 100)
        recommendations.append(SubsidyRecommendation(
            scheme_name="Micro Irrigation Subsidy (PMKSY)",
            potential_benefit=f"Up to ₹{max_benefit:,} ({subsidy_percent}% of cost)",
            eligibility_status="ELIGIBLE",
            description="Subsidy for drip irrigation and sprinkler systems to save water and increase yield.",
            how_to_apply="Apply through Krishi Bhavan or eMISSION portal",
            documents=["Land documents", "Quotation from approved supplier", "Aadhaar", "Bank account"]
        ))
    
    # Farm Mechanization
    if land_size_acres >= 0.5:
        subsidy_percent = 60 if farmer_category in ["sc", "st"] else 50
        recommendations.append(SubsidyRecommendation(
            scheme_name="Farm Mechanization Subsidy (SMAM)",
            potential_benefit=f"Up to ₹1,50,000 ({subsidy_percent}% of equipment cost)",
            eligibility_status="ELIGIBLE",
            description="Subsidy on power tillers, sprayers, pump sets, and other farm machinery.",
            how_to_apply="Apply at agrimachinery.nic.in or Krishi Bhavan",
            documents=["Land documents", "Aadhaar", "Quotation", "Caste certificate if SC/ST"]
        ))
    
    # Organic Farming
    if organic_interest and land_size_acres >= 0.5:
        benefit = int(50000 * land_size_ha)
        recommendations.append(SubsidyRecommendation(
            scheme_name="Organic Farming Subsidy (PKVY)",
            potential_benefit=f"₹{benefit:,} over 3 years",
            eligibility_status="ELIGIBLE (Need cluster of 20+ farmers)",
            description="Support for organic inputs, certification, and marketing. Need to form a cluster with nearby farmers.",
            how_to_apply="Form a farmer group and apply through Krishi Bhavan",
            documents=["Cluster formation documents", "Land records", "Commitment letter"]
        ))
    
    # Interest Subvention
    recommendations.append(SubsidyRecommendation(
        scheme_name="Interest Subvention on Crop Loans",
        potential_benefit="Effective interest rate of just 4% on loans up to ₹3 lakh",
        eligibility_status="ELIGIBLE",
        description="3% interest subvention + additional 3% for prompt repayment on short-term crop loans.",
        how_to_apply="Automatic benefit when taking KCC or crop loan from bank",
        documents=["KCC application or crop loan documents"]
    ))
    
    # PM-KUSUM Solar
    if land_size_acres >= 0.5 and not has_irrigation:
        recommendations.append(SubsidyRecommendation(
            scheme_name="PM-KUSUM Solar Pump Subsidy",
            potential_benefit="60% subsidy on solar pump (up to 7.5 HP)",
            eligibility_status="ELIGIBLE",
            description="Install solar-powered irrigation pump with 60% government subsidy. Save on electricity bills forever.",
            how_to_apply="Apply through ANERT Kerala or Krishi Bhavan",
            documents=["Land documents", "Water source proof", "Aadhaar", "Bank account"]
        ))
    
    # Seed Subsidy
    recommendations.append(SubsidyRecommendation(
        scheme_name="Certified Seed Subsidy",
        potential_benefit="50% subsidy on certified seeds",
        eligibility_status="ELIGIBLE",
        description="Get quality certified seeds at subsidized rates from Krishi Bhavans.",
        how_to_apply="Visit Krishi Bhavan during sowing season",
        documents=["Aadhaar / Ration card", "Land documents"]
    ))
    
    return recommendations
