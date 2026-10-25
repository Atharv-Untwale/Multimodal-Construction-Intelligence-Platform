"""Deterministic sample outputs used when no API key is supplied (demonstration mode)."""

DEMO_SAFETY = {
    "safety_score": 62,
    "overall_status": "Needs Improvement",
    "workers_detected": 5,
    "summary": "Most workers wear helmets and vests, but two workers at an open slab edge lack harnesses "
               "and some wear non-safety footwear. Loose rebar and unguarded edges raise fall risk.",
    "ppe_detection": [
        {"item": "Safety Helmet", "status": "Detected", "compliance_pct": 100, "notes": "All 5 workers wearing helmets."},
        {"item": "High-Vis Vest", "status": "Detected", "compliance_pct": 80, "notes": "4 of 5 wearing vests."},
        {"item": "Steel-Toe Boots", "status": "Missing", "compliance_pct": 60, "notes": "2 workers in non-safety footwear."},
        {"item": "Safety Harness", "status": "Missing", "compliance_pct": 0, "notes": "No harness at slab edge work."},
    ],
    "hazards": [
        {"hazard": "Unprotected slab edge with workers present", "severity": "Critical", "location": "Upper floor, right side",
         "remedy": "Install double-rail edge protection and mandate harness tie-off to anchor points.",
         "standard_reference": "OSHA 1926.501(b)(1); IS 7969"},
        {"hazard": "Protruding rebar without caps", "severity": "High", "location": "Foreground column starters",
         "remedy": "Fit mushroom caps on all exposed vertical bars.", "standard_reference": "OSHA 1926.701(b)"},
        {"hazard": "Debris and loose materials on walkway", "severity": "Medium", "location": "Ground-level access path",
         "remedy": "Daily housekeeping; designate material stacking zones.", "standard_reference": "OSHA 1926.25"},
        {"hazard": "Missing signage for overhead work", "severity": "Low", "location": "Site entrance",
         "remedy": "Post 'Overhead Work' and PPE-mandatory signage.", "standard_reference": "IS 9457"},
    ],
}

DEMO_CRACK = {
    "defect_type": "Settlement",
    "crack_width_mm": 3.5,
    "severity_score": 68,
    "urgency": "Within 7 Days",
    "structural_risk": "High",
    "confidence_pct": 74,
    "summary": "A diagonal, stepped crack of roughly 3.5 mm suggests differential foundation settlement. "
               "Width estimate is approximate without a scale reference.",
    "root_causes": [
        "Differential settlement from poorly compacted or saturated sub-soil",
        "Inadequate foundation depth or bearing area",
        "Nearby excavation or leaking underground pipe softening soil",
    ],
    "recommended_repairs": [
        {"method": "Geotechnical investigation", "details": "Bore logs and SPT to confirm bearing capacity before repair."},
        {"method": "Structural re-grouting", "details": "Cement/micro-concrete grout after stabilising the foundation."},
        {"method": "Epoxy injection", "details": "Low-viscosity epoxy for cracks above 0.3 mm once movement has stopped."},
    ],
    "monitoring_plan": "Install tell-tale crack gauges; record readings fortnightly for 3 months.",
}

CHAT_KEYWORDS = [
    (("cement", "concrete mix", "m25", "grade"),
     "For RCC, M25 is common for residential slabs/columns (IS 456). Typical nominal mix is 1:1:2, but design-mix "
     "with cube tests (7 and 28 day) is preferred. Keep water-cement ratio at or below 0.45 for moderate exposure."),
    (("curing", "cure"),
     "IS 456 recommends curing for at least 7 days (10 days for mineral admixture/hot-weather concrete). "
     "Use wet hessian, ponding or curing compound; start within 24 hours of placement."),
    (("steel", "rebar", "tmt", "fe500"),
     "Use Fe500D TMT bars (IS 1786) for ductility. Maintain clear cover (e.g. 40 mm for columns, 20-30 mm for slabs "
     "under mild exposure), proper lap lengths and bar spacing per the structural drawings."),
    (("crack", "settlement"),
     "Cracks under 0.3 mm are usually cosmetic; wider, stepped or diagonal cracks suggest settlement or shear. "
     "Mark the crack with date-stamped tell-tales and get a structural engineer to inspect."),
    (("safety", "ppe", "helmet", "harness"),
     "Minimum PPE: helmet, high-vis vest, safety shoes; add harness for work above 1.8 m (OSHA) and gloves/eye "
     "protection as needed. Conduct a toolbox talk every morning."),
    (("cost", "budget", "estimate"),
     "Use the Planning tab for an estimate. Always add 5-10% contingency and track cost per sq ft against the "
     "baseline monthly."),
]
CHAT_DEFAULT = ("(Demo mode) I can help with concrete, steel, curing, safety, cracks and cost planning. "
                "Add a Gemini API key in the sidebar for fully contextual answers.")
