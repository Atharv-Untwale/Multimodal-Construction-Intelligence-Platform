"""Central configuration: constants, planning rates and enumerations."""

APP_NAME = "Multimodal Construction Intelligence Platform"
APP_TAGLINE = "Skill Wallet Capstone · Project 1"

MODEL_OPTIONS = ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash"]
DEFAULT_MODEL = MODEL_OPTIONS[0]

MAX_IMAGE_EDGE = 1600          # px, images are downscaled before upload
ALLOWED_IMAGE_TYPES = ["jpg", "jpeg", "png"]

SEVERITY_LEVELS = ["Low", "Medium", "High", "Critical"]
OVERALL_STATUSES = ["Compliant", "Needs Improvement", "Non-Compliant"]
DEFECT_TYPES = ["Hairline", "Settlement", "Structural Shear", "Thermal Expansion", "Spalling"]
URGENCY_LEVELS = ["Monitor", "Within 30 Days", "Within 7 Days", "Immediate"]
PPE_ITEMS = ["Safety Helmet", "High-Vis Vest", "Steel-Toe Boots", "Safety Harness"]

# ---- Indicative planning rates (INR, Tier-2 baseline). Edit freely. ----
STRUCTURE_TYPES = {
    "Residential Apartment": {"cost_psf": 2200, "market_psf": 6500, "steel_kg_psf": 4.0, "cement_bags_psf": 0.40},
    "Independent House / Villa": {"cost_psf": 2600, "market_psf": 7500, "steel_kg_psf": 4.2, "cement_bags_psf": 0.42},
    "Commercial Office": {"cost_psf": 3000, "market_psf": 9000, "steel_kg_psf": 5.0, "cement_bags_psf": 0.45},
    "Industrial Warehouse": {"cost_psf": 1600, "market_psf": 3500, "steel_kg_psf": 6.0, "cement_bags_psf": 0.35},
    "Mixed-Use Complex": {"cost_psf": 2800, "market_psf": 8000, "steel_kg_psf": 4.8, "cement_bags_psf": 0.43},
}

LOCATION_TIERS = {
    "Tier 1 (Mumbai, Delhi NCR, Bengaluru, Chennai)": {"cost_mult": 1.20, "market_mult": 2.20},
    "Tier 2 (Pune, Ahmedabad, Jaipur, Kochi)": {"cost_mult": 1.00, "market_mult": 1.00},
    "Tier 3 (Nashik, Indore, Vijayawada, Mysuru)": {"cost_mult": 0.85, "market_mult": 0.60},
}

CONTINGENCY_PCT = 0.08     # added to base construction cost
LAND_VALUE_SHARE = 0.30    # share of finished market value attributable to land

MILESTONES = [
    (0, 15, "Site prep & foundation"),
    (15, 30, "Plinth & substructure"),
    (30, 60, "RCC superstructure"),
    (60, 75, "Masonry & services rough-in"),
    (75, 95, "Finishing & fit-out"),
    (95, 100, "Testing & handover"),
]

DISCLAIMER = (
    "AI-generated analysis is advisory only and must be verified by a qualified safety officer "
    "or licensed structural engineer before any action is taken."
)
